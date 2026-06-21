# Dark Zurich Validation Set 定性分析推論清單

用 CMA (SegFormer) 官方 Dark Zurich checkpoint 對**完整 Dark Zurich validation set** 推論的結果，供定性分析使用。

## 基本資訊

- 模型：`checkpoints/cma_segformer_darkzurich.ckpt`（CMA + SegFormer MiT-B5，Dark Zurich，test mIoU 53.6）
- 設定檔：`configs/predict_darkzurich.yaml`（`pretrained: null`，權重全由 checkpoint 載入）
- 原始資料集：`/home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon`（val split，未更動）
- 範圍：完整 validation set，共 **50 張**（全部為 night 條件，recording GOPR0356）
- 輸出：19 類 Cityscapes 調色盤彩色圖（mode=P，1920×1080）
- 類別配色：標準 Cityscapes trainId 19 類（道路=紫、人行道=粉、建築=灰、植被=綠、天空=淺藍、人=紅、車=深藍 等）

## 結果位置

- 彩色結果圖：`qual_results_darkzurich/night/<檔名>.png`
- 機器可讀清單：`qual_results_darkzurich/manifest.csv`
- 原始 predict 輸出（含未上色 trainId 灰階圖）：`logs/cma_segformer_darkzurich/lightning_logs/version_0/`

> 結果圖檔名沿用原始影像檔名，方便一一對應。

## Night（50 張）

| # | 結果圖 (`qual_results_darkzurich/night/`) | 原始影像路徑 |
|---|---|---|
| 1 | GOPR0356_frame_000321_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000321_rgb_anon.png |
| 2 | GOPR0356_frame_000324_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000324_rgb_anon.png |
| 3 | GOPR0356_frame_000327_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000327_rgb_anon.png |
| 4 | GOPR0356_frame_000330_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000330_rgb_anon.png |
| 5 | GOPR0356_frame_000333_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000333_rgb_anon.png |
| 6 | GOPR0356_frame_000336_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000336_rgb_anon.png |
| 7 | GOPR0356_frame_000339_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000339_rgb_anon.png |
| 8 | GOPR0356_frame_000342_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000342_rgb_anon.png |
| 9 | GOPR0356_frame_000345_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000345_rgb_anon.png |
| 10 | GOPR0356_frame_000348_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000348_rgb_anon.png |
| 11 | GOPR0356_frame_000351_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000351_rgb_anon.png |
| 12 | GOPR0356_frame_000354_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000354_rgb_anon.png |
| 13 | GOPR0356_frame_000357_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000357_rgb_anon.png |
| 14 | GOPR0356_frame_000360_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000360_rgb_anon.png |
| 15 | GOPR0356_frame_000363_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000363_rgb_anon.png |
| 16 | GOPR0356_frame_000366_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000366_rgb_anon.png |
| 17 | GOPR0356_frame_000369_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000369_rgb_anon.png |
| 18 | GOPR0356_frame_000372_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000372_rgb_anon.png |
| 19 | GOPR0356_frame_000375_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000375_rgb_anon.png |
| 20 | GOPR0356_frame_000378_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000378_rgb_anon.png |
| 21 | GOPR0356_frame_000382_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000382_rgb_anon.png |
| 22 | GOPR0356_frame_000386_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000386_rgb_anon.png |
| 23 | GOPR0356_frame_000391_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000391_rgb_anon.png |
| 24 | GOPR0356_frame_000395_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000395_rgb_anon.png |
| 25 | GOPR0356_frame_000398_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000398_rgb_anon.png |
| 26 | GOPR0356_frame_000401_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000401_rgb_anon.png |
| 27 | GOPR0356_frame_000404_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000404_rgb_anon.png |
| 28 | GOPR0356_frame_000408_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000408_rgb_anon.png |
| 29 | GOPR0356_frame_000414_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000414_rgb_anon.png |
| 30 | GOPR0356_frame_000418_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000418_rgb_anon.png |
| 31 | GOPR0356_frame_000421_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000421_rgb_anon.png |
| 32 | GOPR0356_frame_000424_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000424_rgb_anon.png |
| 33 | GOPR0356_frame_000427_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000427_rgb_anon.png |
| 34 | GOPR0356_frame_000430_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000430_rgb_anon.png |
| 35 | GOPR0356_frame_000433_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000433_rgb_anon.png |
| 36 | GOPR0356_frame_000437_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000437_rgb_anon.png |
| 37 | GOPR0356_frame_000448_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000448_rgb_anon.png |
| 38 | GOPR0356_frame_000452_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000452_rgb_anon.png |
| 39 | GOPR0356_frame_000455_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000455_rgb_anon.png |
| 40 | GOPR0356_frame_000458_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000458_rgb_anon.png |
| 41 | GOPR0356_frame_000461_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000461_rgb_anon.png |
| 42 | GOPR0356_frame_000464_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000464_rgb_anon.png |
| 43 | GOPR0356_frame_000467_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000467_rgb_anon.png |
| 44 | GOPR0356_frame_000470_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000470_rgb_anon.png |
| 45 | GOPR0356_frame_000473_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000473_rgb_anon.png |
| 46 | GOPR0356_frame_000476_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000476_rgb_anon.png |
| 47 | GOPR0356_frame_000479_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000479_rgb_anon.png |
| 48 | GOPR0356_frame_000482_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000482_rgb_anon.png |
| 49 | GOPR0356_frame_000485_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000485_rgb_anon.png |
| 50 | GOPR0356_frame_000488_rgb_anon.png | /home/rvl1421/Datasets/Dark_Zurich/Dark_Zurich_val_anon/rgb_anon/val/night/GOPR0356/GOPR0356_frame_000488_rgb_anon.png |
