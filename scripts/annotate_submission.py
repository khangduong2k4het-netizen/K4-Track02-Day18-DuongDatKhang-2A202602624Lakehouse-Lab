"""Add explanations without altering measured cell outputs."""
from pathlib import Path
import nbformat
ROOT = Path(__file__).resolve().parents[1]
notes = [
    'Ghi sai age="thirty" bị chặn bằng lỗi cast Int64 thực tế. schema_mode="merge" thêm tier; các dòng cũ có null. JSON commit là bằng chứng transaction log; cờ schema đã được sửa để phản ánh exception thật.',
    'Compaction giảm chi phí mở file. Z-order thu hẹp min/max user_id nên query điểm chỉ cần một file trong 55 file. Pruning 55× vượt ngưỡng 10×; thời gian wall-clock phụ thuộc cache và tải máy, vì vậy cần đọc số speedup của lần chạy này trong output.',
    'MERGE có 100.000 dòng nguồn: 50.000 update và 50.000 insert. RESTORE tạo version mới v4, giữ lịch sử v0–v3. Sau restore không còn score âm; time travel vẫn đọc được version cũ khi các file còn được giữ.',
    'Silver loại 9.948 dòng trùng từ 200.000 dòng Bronze, còn 190.052. Gold có 8 ngày × 3 model = 24 dòng. Kiểm tra bổ sung xác nhận đủ cặp, không null, p50 ≤ p95, cost dương và error_rate trong [0,1]. Giá token là giá minh họa trong lab.',
    'Lọc trên ts làm Iceberg suy ra day(ts), đọc 1/10 file: pruning 10×. Rename latency_ms giữ field ID 4 nên không cần ghi lại dữ liệu. Hai spec ID cùng tồn tại và 5.500 dòng đọc được. Metadata/data gần 293% với tập nhỏ cho thấy nhiều file nhỏ có overhead lớn.',
    'Compaction giảm 200 xuống 11 file; clustering cho phép bỏ qua 90% file. Vacuum thu hồi file tombstoned, không tìm được orphan chưa commit; phép hiệu file trên đĩa và file được tham chiếu cần age guard để bảo vệ writer. Expiry giảm 20 xuống 3 snapshots nhưng phải sweep 17 manifest lists để thu hồi dung lượng. Đây là hành vi engine/version của lab; retention 0 chỉ dùng với scratch.',
    'Random-read inline chịu granularity row group nên amplification 200×; projection scan cột nhỏ vẫn có thể bỏ qua blob. Int8 nhỏ 5,8×, recall@10 0,904 và topic fidelity 1,000 trên corpus giả. External index vẫn giữ 8 tài liệu bị xóa trong bảng: pipeline phải xử lý CDF delete, không chỉ upsert. Vector Delta đọc về list cần cast trước truy vấn DuckDB.',
    'Silver có hai partition policy-v2/v3. Pin version 0 tái lập 1.578 bước, trong khi version mới có 1.978; replay ở đây chỉ so số bước, chưa so nội dung. Cache list_tables giảm 5 lượt xuống 1 catalog read. MCP/task/confirmation chỉ mô phỏng offline; confirmed do caller truyền. Bốn bucket provenance là mapping minh họa, không xác minh quyền sử dụng; CC-BY cần ghi công. Xóa subject ở version hiện tại không xóa bản lịch sử.'
]
for file, note in zip(sorted((ROOT / 'submission/notebooks').glob('*.ipynb')), notes):
    nb = nbformat.read(file, 4)
    nb.cells.append(nbformat.v4.new_markdown_cell('## Giải thích kết quả (Codex hỗ trợ)\n\n' + note))
    nbformat.write(nb, file)
    nbformat.write(nb, ROOT / 'notebooks' / file.name)
