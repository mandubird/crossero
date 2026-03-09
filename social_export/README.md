# SNS Batch Export (One Click)

## What this does
- Double-click one file: `Run_SNS_Image_Batch.command`
- Reads puzzle IDs from `queue/` file names (example: `gen_001.txt`)
- Creates 9 images per puzzle:
  - Types: `puzzle`, `hint`, `answer`
  - Ratios: `square(1:1)`, `vertical(9:16)`, `landscape(4:3)`
- Adds branding on every image:
  - Logo
  - `crossero.com`
  - `십자가로세로`

## Folder structure
- `queue/` : put empty files named with puzzle ID
- `queue_done/` : processed queue files are moved here
- `output/` : generated images
- `logs/` : run logs

Output example:
- `output/20260309_223000_gen_001_창세기-천지창조/`
- `output/20260309_223000_gen_001_창세기-천지창조/square/puzzle.png`
- `output/20260309_223000_gen_001_창세기-천지창조/square/hint.png`
- `output/20260309_223000_gen_001_창세기-천지창조/square/answer.png`
- `output/20260309_223000_gen_001_창세기-천지창조/vertical/...`
- `output/20260309_223000_gen_001_창세기-천지창조/landscape/...`

## Usage
1. Create empty files in `queue/` with puzzle IDs.
2. Double-click `Run_SNS_Image_Batch.command`.
3. Use images in `output/` for Pinterest / Naver Blog / X(Twitter) / Instagram.

## Notes
- Puzzle ID must exist in `data.js`.
- If a queue file fails, it is moved to `queue_done/*.failed`.
- Logs are written to `logs/run_YYYYMMDD.log`.
