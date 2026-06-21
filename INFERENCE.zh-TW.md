# 推論與視覺化（你的使用情境）

你要的就是：拿資料集 → 用官方訓練好的權重做推論 → 跑出彩色視覺化結果。這份文件只講這件事。

底下大部分東西我已經幫你準備好了，你真正還要自己做的只有一件：**用你的帳號去下載資料集**（這些資料集都需要註冊/同意條款，沒辦法幫你抓）。

---

## 我已經弄好的部分

- **conda 環境 `cma`**：已驗證能在你的 RTX 4090 上跑 GPU 推論。
- **三個官方 checkpoint**（各 1.4GB，已下載、已驗證完整）：
  - `checkpoints/cma_segformer_acdc.ckpt`
  - `checkpoints/cma_segformer_darkzurich.ckpt`
  - `checkpoints/cma_segformer_robotcar.ckpt`
- **三份推論專用 config**（`pretrained` 已設為 `null`，所以不需要再去抓 SegFormer 的 Google Drive 權重，權重全部由 checkpoint 載入）：
  - `configs/predict_acdc.yaml`
  - `configs/predict_darkzurich.yaml`
  - `configs/predict_robotcar.yaml`
- 整條推論+視覺化流程我已經用合成影像實際跑過一次，確認能正常輸出彩色 PNG。

---

## 你要做的部分

### 步驟 1：每次開終端機先設定環境

```bash
conda activate cma
export DATA_DIR=$HOME/cma_data       # 資料集都放這底下；要換位置就改這個路徑
```

### 步驟 2：下載資料集（只有這步要你自己來）

資料集要放到 `$DATA_DIR` 底下，資料夾名稱和結構要跟 [README](README.md) 對得起來。推論只用到 **val 分割**，所以其實不必下載 train 那包大檔。

- **ACDC**：到 [ACDC 下載頁](https://acdc.vision.ee.ethz.ch/download)（要註冊帳號）抓 `rgb_anon_trainvaltest.zip`，解壓到 `$DATA_DIR/ACDC`。結構長這樣：
  ```
  $DATA_DIR/ACDC/rgb_anon/{fog,night,rain,snow}/val/<recording>/*_rgb_anon.png
  $DATA_DIR/ACDC/gt/{fog,night,rain,snow}/val/         # 這個資料夾要存在（程式會檢查），裡面有沒有東西都行
  ```
- **Dark Zurich**：到 [這裡](https://www.trace.ethz.ch/publications/2019/GCMA_UIoU/)抓 `Dark_Zurich_val_anon.zip`，解壓到 `$DATA_DIR/DarkZurich`。
- **RobotCar**：依 [README 的 RobotCar 段落](README.md#download-the-data)從那幾個來源抓，放到 `$DATA_DIR/RobotCar`。

### 步驟 3：跑推論

挑你要的資料集，下對應指令就好：

```bash
# ACDC
python -m tools.run predict --config configs/predict_acdc.yaml \
    --trainer.accelerator gpu --trainer.devices 1 \
    --ckpt_path checkpoints/cma_segformer_acdc.ckpt

# Dark Zurich
python -m tools.run predict --config configs/predict_darkzurich.yaml \
    --trainer.accelerator gpu --trainer.devices 1 \
    --ckpt_path checkpoints/cma_segformer_darkzurich.ckpt

# RobotCar
python -m tools.run predict --config configs/predict_robotcar.yaml \
    --trainer.accelerator gpu --trainer.devices 1 \
    --ckpt_path checkpoints/cma_segformer_robotcar.ckpt
```

### 步驟 4：看結果

輸出會在這裡（`<dataset>` 是 ACDC / DarkZurich / RobotCar）：

```
logs/<config 名稱>/lightning_logs/version_0/color_preds/<dataset>/*.png   ← 彩色視覺化（你要的）
logs/<config 名稱>/lightning_logs/version_0/preds/<dataset>/*.png         ← 灰階 trainId 標籤圖
```

`color_preds/` 就是上好色的分割圖，用 Cityscapes 的標準配色（道路紫、人紅、車深藍等等）。

---

## 幾個要知道的點

- **第一次跑會先卡個十幾秒**：那是在用 ninja 即時編譯一個自訂 CUDA 運算子，編完會快取，之後就不會再等。
- **輸出固定 19 類**：模型在 Cityscapes 類別上訓練，不管丟什麼街景進去，分出來的都是那 19 類（道路、人行道、建築、人、車……）。
- **想直接看官方範例、連資料集都不想下載？** ETH 有提供算好的彩色預測圖，可以直接抓來看：
  ```bash
  # ACDC val 的官方彩色預測（約 8.7MB）
  curl -L -o acdc_colored_preds.zip \
    "https://www.research-collection.ethz.ch/server/api/core/bitstreams/4ee42b14-588b-41a4-a805-805b168e9870/content"
  unzip acdc_colored_preds.zip
  ```
  （Dark Zurich、RobotCar 的對應檔也在同一個 ETH 典藏裡。）

- **重跑會開新的 version 資料夾**：第二次跑同一個 config，輸出會進 `version_1`，不會蓋掉上一次。
