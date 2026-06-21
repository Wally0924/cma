# CMA 執行指南（繁體中文）

這份文件整理「環境已經建好之後」要怎麼跑這個模型，以及如果你想用**自己的資料**，需要準備哪些東西、下哪些指令。

環境本身已經裝在 conda 的 `cma` 環境裡（torch 2.0.1+cu118，相容你的 RTX 4090）。每次開新終端機都要先：

```bash
conda activate cma
export DATA_DIR=/path/to/your/data   # 所有資料集都放這個資料夾底下，程式啟動時就會讀這個變數
```

`DATA_DIR` 沒設的話，連 import 都會直接報 `KeyError: 'DATA_DIR'`，這不是 bug，是它的設計。

---

## 先決定你要做哪一件事

「用自己的資料集跑他們的模型」其實有三種不同的目標，需要的東西差很多。先對號入座：

| 情境 | 你想做的事 | 要不要標註 (ground truth) | 要不要成對影像 |
|------|-----------|--------------------------|----------------|
| **A. 推論** | 拿官方訓練好的權重，對我自己的影像輸出分割結果圖 | 不用 | 不用 |
| **B. 測分數** | 在標準 benchmark（ACDC 等）上重現論文的 mIoU | 要（trainId 格式） | 不用 |
| **C. 訓練適應** | 在我自己的資料上跑 CMA 的「正常→惡劣天候」模型適應訓練 | 不用（會自動產生 pseudo-label） | **要** |

最常見的是情境 A。情境 C 是這篇論文的核心方法，但它有一個硬性前提：**訓練資料必須是成對的**——同一個地點、一張惡劣天候、一張正常天候。沒有成對影像就沒辦法跑 CMA 的對比學習，這點先講清楚，免得後面白做工。

---

## 不管哪個情境，都要先下載的權重

### 1. SegFormer 的 Cityscapes 預訓練權重（必備）

模型在初始化時就會去讀這個檔案，缺檔會直接報錯，連用現成 checkpoint 測試都不行。

- 檔名：`segformer.b5.1024x1024.city.160k.pth`
- 來源：[SegFormer 官方 repo](https://github.com/NVlabs/SegFormer)（README 裡有 Google Drive 連結）
- 放這裡：`./pretrained_models/segformer.b5.1024x1024.city.160k.pth`

```bash
mkdir -p pretrained_models
# 把下載好的 .pth 放進 pretrained_models/
```

VGG（ImageNet）和對齊網路（MegaDepth）的權重程式會自己從網路抓，不用手動處理。

### 2. CMA 的模型 checkpoint（情境 A、B 需要）

官方提供四組 `.ckpt`，在 [README 的表格](README.md#model-checkpoints-and-results)裡。例如 SegFormer + ACDC 那一組，下載後放哪裡都行，等下用 `--ckpt_path` 指過去就好。

---

## 情境 A：用官方權重對自己的影像出分割圖

這是門檻最低的做法。`predict` 模式只吃影像、不需要標註，輸出每張圖的分割結果（19 類 Cityscapes 類別）。

它的資料集是寫死在程式裡的（`ACDC`、`DarkZurich`、`RobotCar`、`ACG`），所以你得自己加一個讀你影像的 dataset 類別。三個步驟：

**步驟 1**：把影像放到 `$DATA_DIR/MyDataset/images/` 底下。

**步驟 2**：新增 `data_modules/datasets/mydataset.py`，照現成 dataset 的格式寫一個最小版本：

```python
import os
from PIL import Image
import torch


class MyDataset(torch.utils.data.Dataset):

    orig_dims = (1080, 1920)   # 改成你影像的原始 (高, 寬)

    def __init__(self, root, stage="predict", load_keys=["image"],
                 transforms=None, predict_on="test", **kwargs):
        super().__init__()
        self.root = root
        self.transforms = transforms
        self.load_keys = [load_keys] if isinstance(load_keys, str) else load_keys
        img_dir = os.path.join(root, "images")
        self.paths = {"image": [os.path.join(img_dir, f)
                                for f in sorted(os.listdir(img_dir))]}

    def __getitem__(self, index):
        sample = {"filename": os.path.basename(self.paths["image"][index])}
        for k in self.load_keys:
            sample[k] = Image.open(self.paths[k][index]).convert("RGB")
        if self.transforms is not None:
            sample = self.transforms(sample)
        return sample

    def __len__(self):
        return len(self.paths["image"])
```

**步驟 3**：把它註冊起來，有兩個地方要改：

- `data_modules/datasets/__init__.py` 加一行：
  ```python
  from .mydataset import MyDataset
  ```
- `data_modules/combined_data_module.py` 的 `self.data_dirs` 字典裡加一筆（不加會 KeyError）：
  ```python
  'MyDataset': os.path.join(DATA_DIR, 'MyDataset'),
  ```

**步驟 4**：複製一份 config（例如 `configs/cma_segformer_acdc.yaml`）改成 `configs/my_predict.yaml`，把 `predict:` 區塊換成你的 dataset：

```yaml
      predict:
        MyDataset:
          predict_on: test
          load_keys:
            - image
          transforms:
            - class_path: data_modules.transforms.ToTensor
            - class_path: data_modules.transforms.ConvertImageDtype
            - class_path: data_modules.transforms.Normalize
```

**步驟 5**：跑起來：

```bash
python -m tools.run predict \
    --config configs/my_predict.yaml \
    --trainer.accelerator gpu \
    --ckpt_path /path/to/cma_segformer_acdc.ckpt
```

輸出會存在 checkpoint 旁邊：`preds/`（trainId 灰階圖）和 `color_preds/`（上色後的彩色圖）。

一個提醒：不管你的影像是什麼場景，輸出永遠是 Cityscapes 那 19 類（道路、人、車……）。模型只認得它被訓練過的類別。

---

## 情境 B：在標準資料集上重現論文分數

跟情境 A 幾乎一樣，差別是改用 `test` 模式，而且需要有 ground truth 標註（`gt` 資料夾、`labelTrainIds` 格式）才能算 mIoU。資料夾結構照 [README](README.md) 裡每個資料集的說明擺好就行。

```bash
python -m tools.run test \
    --config configs/cma_segformer_acdc.yaml \
    --trainer.accelerator gpu \
    --ckpt_path /path/to/cma_segformer_acdc.ckpt
```

ACDC 和 Dark Zurich 的這個指令算的是 validation 分數；正式 test 分數要把 `predict` 出來的結果上傳到官方評測伺服器。

---

## 情境 C：在自己的資料上訓練 CMA

這是完整的模型適應訓練。要能跑，你的資料得湊齊三樣東西：

1. **成對影像**：每個地點一張惡劣天候（`image`）、一張正常天候參考（`image_ref`）。CMA 靠這兩張的對應關係做對比學習，這是整個方法的根。
2. **Pseudo-label**：由 source model 對惡劣天候影像產生的偽標註，當作 `semantic`。
3. **預訓練權重**：上面那個 SegFormer Cityscapes `.pth`。

你的 dataset 類別要比情境 A 多回傳 `image_ref` 和 `semantic`，可以直接參考 [`data_modules/datasets/acdc.py`](data_modules/datasets/acdc.py) 的寫法——它示範了怎麼把惡劣影像對到參考影像、怎麼讀 pseudo-label。`orig_dims` 也要設成你影像的尺寸。

Pseudo-label 有兩種來路：

- **自己產生**（針對自訂資料只能走這條）：
  ```bash
  python -m tools.run generate_pl \
      --config configs/my_train.yaml \
      --trainer.accelerator gpu
  ```
- **用官方預先算好的**：只有 ACDC 有，第一次訓練時會自動下載，自訂資料用不到。

產生好 pseudo-label 之後，開始訓練：

```bash
python -m tools.run fit \
    --config configs/my_train.yaml \
    --trainer.accelerator gpu \
    --trainer.precision 16
```

訓練大概要 20 GB 左右的顯卡記憶體。你的 4090 有 24 GB，剛好夠，但如果同時開其他吃顯存的東西可能會 OOM。

---

## 指令速查

```bash
# 每次都要先做
conda activate cma
export DATA_DIR=/path/to/your/data

# 推論：對自己的影像出分割圖（情境 A）
python -m tools.run predict --config configs/my_predict.yaml \
    --trainer.accelerator gpu --ckpt_path /path/to/model.ckpt

# 測試：算 mIoU 分數（情境 B）
python -m tools.run test --config configs/cma_segformer_acdc.yaml \
    --trainer.accelerator gpu --ckpt_path /path/to/model.ckpt

# 產生 pseudo-label（情境 C 第一步）
python -m tools.run generate_pl --config configs/my_train.yaml \
    --trainer.accelerator gpu

# 訓練（情境 C）
python -m tools.run fit --config configs/my_train.yaml \
    --trainer.accelerator gpu --trainer.precision 16

# 看某個子指令有哪些參數
python -m tools.run fit --help

# 環境自我檢查（確認 GPU、各模組、CUDA 擴充都正常）
python -m tools.env_test
```

---

## 已知地雷

- **`generate_pl` 有一個上游 bug**：[`helpers/pseudo_labels.py`](helpers/pseudo_labels.py) 第 65 行寫成 `os.environ['$DATA_DIR']`（多了一個 `$`），執行到存檔那步會丟 `KeyError: '$DATA_DIR'`。要自己產生 pseudo-label 的話，把它改成 `os.environ['DATA_DIR']` 就好。情境 A、B 不會碰到這行。
- **改了 dataset 類別卻忘了註冊**：config 裡的名稱是靠 `globals()[名稱]` 去找類別的，所以 `datasets/__init__.py` 的 import 和 `combined_data_module.py` 的 `data_dirs` 兩邊都要加，少一邊就會報錯。
- **類別數固定是 19**：config 裡的 `num_classes: 19` 對應 Cityscapes。除非你重新訓練一個不同類別的 source model，否則就維持 19。
- **第一次跑 predict / fit 會卡一下**：那個自訂 CUDA 相關性運算子是第一次執行才用 ninja 即時編譯的，編完會快取，第二次就不會等了。
