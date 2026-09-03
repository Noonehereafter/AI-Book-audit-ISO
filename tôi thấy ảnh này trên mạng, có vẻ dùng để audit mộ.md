<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# tôi thấy ảnh này trên mạng, có vẻ dùng để audit một bản dịch AI. nếu tôi muốn áp dụng cách tương tự để audit bản dịch sách bằng AI nhưng với một hệ thống lớn hơn, chi tiết hơn, hay và trau chuốt thì nên nghiên cứu audit ở những mặt nào một cách phổ quát

Đúng: ảnh này đang dùng một dạng **bảng đối chiếu/audit chất lượng** giữa bản dịch AI và bản master, nhưng nó mới thiên về “so sánh kết quả cuối” và một số lỗi có thể đếm được. Nếu áp dụng cho sách—đặc biệt tiểu thuyết dịch bằng AI—anh/chị nên xây một hệ thống audit đa tầng: kiểm đúng nghĩa, kiểm tính nhất quán toàn tác phẩm, kiểm chất văn, kiểm tính toàn vẹn EPUB và kiểm rủi ro xuất bản.[^1_1]

Khung phù hợp nhất để làm nền là MQM/ISO 5060: đánh giá song ngữ theo loại lỗi, mức độ nghiêm trọng, điểm phạt và xếp hạng chất lượng. ISO 5060 áp dụng rõ cho cả bản dịch người, MT hậu biên tập và MT chưa hậu biên tập; MQM có bảy nhóm lớn gồm thuật ngữ, chính xác nội dung, quy ước ngôn ngữ, phong cách, bản địa hóa, mức phù hợp với độc giả, và thiết kế/markup.[^1_2][^1_3]

## Tư duy thiết kế hệ thống

Đừng coi audit là một prompt “chấm xem bản dịch có hay không”. Với sách dài, hệ thống tốt cần trả lời đồng thời năm câu hỏi:

1. **Bản dịch có đúng với nguyên tác không?**
2. **Có nhất quán từ chương đầu đến chương cuối không?**
3. **Có đọc như một tác phẩm tiếng Việt tự nhiên, đúng thể loại không?**
4. **Có giữ nguyên cấu trúc, metadata, chú thích và khả năng xuất bản của ebook không?**
5. **Các lỗi tìm thấy có được quản trị để sửa, học lại và ngăn tái diễn trong các chương sau không?**

Vì thế, hãy tách audit thành ba lớp:


| Lớp | Mục tiêu | Đơn vị kiểm | Cách kiểm phù hợp |
| :-- | :-- | :-- | :-- |
| Gate tự động | Chặn lỗi khách quan, lặp lại, lỗi kỹ thuật | Toàn bộ sách | Regex, parser EPUB/HTML, đối chiếu số liệu, glossary matcher, kiểm cấu trúc |
| QA ngữ nghĩa bằng AI | Phát hiện lỗi nghĩa, logic, giọng văn, mạch truyện | Segment/đoạn/chương | AI đối chiếu nguồn–đích, RAG với knowledge base |
| Review biên tập | Ra quyết định với lỗi tinh tế và chuẩn xuất bản | Mẫu đại diện + điểm rủi ro cao | Người biên tập hoặc AI reviewer có rubric cực chặt |

**AI không nên vừa là người dịch vừa là người tự chấm độc lập duy nhất.** Cần dùng model/prompt/vai trò audit khác với pipeline dịch; tốt hơn nữa là dùng “hội đồng” 2–3 reviewer AI và cơ chế phân xử khi kết quả bất đồng.

## Bộ tiêu chí phổ quát

### 1. Độ trung thực với nguyên tác

Đây là nhóm “không thể hy sinh”, có thể map trực tiếp với MQM/ISO 5060: sai dịch, bỏ sót, thêm ý, không dịch, và sai thuật ngữ.[^1_3][^1_4]

Nên audit cụ thể các dạng sau:

- **Sai nghĩa trực tiếp:** dịch nhầm chủ thể, hành động, quan hệ nhân quả, tình thái, phủ định, thời–thể, mức độ chắc chắn.
- **Bỏ sót:** mất câu, mệnh đề, chi tiết miêu tả, thông tin nền, chữ trong ngoặc, lời độc thoại, đoạn chuyển cảnh.
- **Thêm diễn giải:** AI tự giải thích, tự làm rõ, thêm động cơ tâm lý hay tình tiết không có trong nguyên tác.
- **Dịch thiếu/sai quan hệ:** who/whom, đại từ quy chiếu, quan hệ gia tộc, phe phái, chủ sở hữu, người đang nói.
- **Sai thực thể:** tên người, địa danh, môn phái, tổ chức, đồ vật, công pháp, chức vị, niên hiệu, điển cố.
- **Số liệu và logic cứng:** tiền, tuổi, mốc thời gian, thứ hạng, cấp bậc, tỷ lệ, khoảng cách, số chương, tên kỹ năng.
- **Đoạn chưa dịch hoặc dịch lẫn ngôn ngữ nguồn:** đặc biệt trong câu thoại, tiêu đề, ghi chú ảnh, bảng, nội dung HTML/EPUB.

Với tiểu thuyết, nên bổ sung hai nhãn lỗi mà các framework chung thường chưa làm đủ rõ:

- **Sai tiền đề truyện:** dịch làm hỏng thông tin mà độc giả cần để hiểu một sự kiện ở chương hiện tại hoặc chương sau.
- **Spoiler do diễn giải:** bản dịch nói quá rõ một ẩn ý mà nguyên tác còn cố tình giữ mơ hồ.


### 2. Nhất quán cấp tác phẩm

Bảng trong ảnh đã có thuật ngữ, xưng hô và chú thích—đó là đúng hướng. Nhưng hệ thống lớn phải audit bằng **bộ nhớ có cấu trúc**, không chỉ bằng tìm–thay từ vựng.[^1_1]

Hãy xây “Translation Bible”/knowledge base cho từng bộ sách, bao gồm:


| Nhóm dữ liệu | Cần lưu và audit |
| :-- | :-- |
| Thực thể | Tên gốc, tên Việt hóa, alias, phiên âm, giới tính, vai trò, quan hệ |
| Xưng hô | Ma trận ai gọi ai thế nào, theo giai đoạn quan hệ, bối cảnh trang trọng/thân mật |
| Thuật ngữ | Thuật ngữ nguồn, bản dịch chuẩn, biến thể cấm, chú giải, lần xuất hiện đầu |
| Thế giới truyện | Cảnh giới, hệ thống sức mạnh, địa danh, tổ chức, lịch sử, quy tắc vận hành |
| Dòng thời gian | Sự kiện, thời điểm, tuổi, thứ tự chương, flashback/foreshadowing |
| Giọng nhân vật | Từ vựng, nhịp câu, mức trang trọng, tật nói, độ cổ phong hoặc hiện đại |
| Quy ước biên tập | Dấu thoại, tên chương, viết hoa, phiên âm, chú thích, cách xử lý thơ/câu đối |

Các chỉ số nên đo toàn sách:

- Tỷ lệ thuật ngữ dùng đúng glossary.
- Số biến thể không được phép của cùng một thực thể/thuật ngữ.
- Số vi phạm xưng hô theo ma trận quan hệ.
- Số thay đổi giọng nói bất thường theo nhân vật.
- Số mâu thuẫn số liệu, thời gian, giới tính, cấp bậc hoặc quan hệ.
- Số chú thích lặp, thiếu, sai chuẩn hoặc xuất hiện không đúng lần đầu cần giải thích.

Điểm quan trọng: **một lỗi thuật ngữ không phải lúc nào cũng bằng nhau**. Dịch sai một vật dụng nhỏ một lần có thể là Minor; đổi tên cảnh giới hoặc xưng hô trung tâm của nhân vật xuyên 30 chương là Major, thậm chí Critical.

### 3. Chất lượng tiếng Việt và chất văn

“Không lỗi ngữ pháp” không đồng nghĩa “đọc hay”. MQM tách riêng lỗi về quy ước ngôn ngữ với lỗi phong cách; nhóm phong cách bao gồm các trường hợp câu đúng ngữ pháp nhưng không phù hợp style guide hoặc không đúng ngữ cảnh độc giả.[^1_3]

Đối với bản dịch sách, audit riêng các hạng mục:

- **Độ tự nhiên:** có dấu vết dịch sát cấu trúc tiếng nguồn không; câu có “Tây hóa/Hán hóa” vô thức, rườm rà hoặc cứng không.
- **Độ mượt và nhịp văn:** câu dài–ngắn có chủ ý; liên kết đoạn; tránh lặp cấu trúc “hắn không khỏi”, “khẽ cười nói”, “lập tức”, “không ngờ rằng” dày đặc.
- **Đúng register:** cổ phong, lịch sử, kiếm hiệp, kinh dị, trinh thám, romance, sci-fi hay phi hư cấu cần những quy tắc ngôn ngữ khác nhau.
- **Giọng trần thuật:** nhất quán giữa chương, không bị model “đổi văn phong” do chia chunk.
- **Phân biệt giọng nhân vật:** người già, võ tướng, học giả, trẻ con, nhân vật hiện đại, nhân vật quyền lực phải có đặc trưng đủ rõ nhưng không biếm họa.
- **Hàm ý và sắc thái:** mỉa mai, đe dọa, gợi tình, bi thương, hài hước, lạnh lùng, lễ nghi, tâm lý ngầm.
- **Mức độ can thiệp:** bản dịch không được tự “văn vẻ hóa” mọi câu đến mức đổi tính cách tác giả, cũng không được bám chữ đến vô hồn.
- **Lặp từ và nghèo từ vựng:** audit theo cửa sổ 1 đoạn, 1 chương và toàn sách; phân biệt lặp có chủ ý với lặp do AI.
- **Dấu câu và thoại:** thống nhất gạch đầu dòng/dấu ngoặc kép, lời dẫn thoại, suy nghĩ, tin nhắn, thư từ, thơ, câu đối.

Một tiêu chí rất hữu ích là **“đọc độc lập không cần nguyên tác”**: đưa riêng bản tiếng Việt cho một reviewer AI, yêu cầu đánh giá khả năng hiểu, nhịp truyện, nhân vật, lỗi logic bề mặt và cảm giác “dịch máy”. Sau đó đối chiếu với audit song ngữ. Nếu song ngữ đạt cao nhưng độc lập đọc vẫn gượng, vấn đề nằm ở biên tập tiếng Việt chứ không phải độ chính xác.

### 4. Văn hóa, bản địa hóa và chú giải

MQM coi quy ước bản địa, mức phù hợp với độc giả và design/markup là các chiều độc lập; điều này rất phù hợp với sách dịch, nơi “đúng nghĩa” vẫn có thể gây sai trải nghiệm đọc.[^1_5][^1_3]

Audit các quyết định biên tập cấp sách:

- **Chiến lược tên riêng:** giữ Hán–Việt, pinyin, Việt hóa, dịch nghĩa hay kết hợp—và có áp dụng nhất quán không.
- **Điển cố/văn hóa:** chỗ nào cần chú thích, chỗ nào nên nội hóa nhẹ vào câu, chỗ nào phải giữ độ xa lạ của nguyên tác.
- **Đơn vị đo lường, tiền tệ, lịch pháp:** giữ nguyên và chú thích, hay quy đổi; quy tắc cần được khóa từ đầu.
- **Tước vị, chức quan, cách gọi:** phân biệt khi nào dịch nghĩa, âm Hán–Việt hoặc giữ tên gốc.
- **Nội dung nhạy cảm:** bạo lực, tình dục, phân biệt đối xử, tôn giáo, chính trị, trẻ vị thành niên—không tự ý kiểm duyệt hoặc làm nhẹ nếu không có editorial policy đã phê duyệt.
- **Chú thích:** đúng, cần thiết, không spoil, không lặp, không làm vỡ nhịp đọc.

Nên viết trước một **Editorial Policy**: độc giả mục tiêu, mức chú thích, phong cách Việt hóa, quy tắc xưng hô, mức cổ phong, danh từ riêng, cách xử lý nội dung nhạy cảm. Không có tài liệu này, hai reviewer audit cùng một câu có thể chấm trái ngược nhưng đều “có lý”.

### 5. Toàn vẹn xuất bản số

Ảnh có nhắc tỷ lệ văn bản và chú thích; với EPUB thực tế, phần này cần được nâng thành một gate kỹ thuật riêng.[^1_1]

Kiểm toàn bộ file, không lấy mẫu:

- Không mất/chèn/chồng đoạn, tiêu đề, epigraph, thơ, bảng, thư, ghi chú cuối trang.
- Số chương, thứ tự chapter, liên kết mục lục/NCX/nav, anchor nội bộ, ảnh và caption đúng.
- Thẻ HTML, CSS, class, id, thuộc tính `href`, ký tự escape, entity không hỏng.
- Không làm thay đổi placeholder, biến, ký hiệu định dạng, markdown/HTML inline.
- Không có đoạn nguồn còn sót, bản dịch trùng lặp, chunk bị lặp đầu/cuối.
- Metadata: tác giả, dịch giả, series, số tập, ngôn ngữ, mô tả, bìa, ISBN nếu có.
- Khả năng hiển thị trên Calibre, Kindle Previewer/thiết bị mục tiêu, app đọc Android/iOS.
- So sánh độ dài theo chapter và phát hiện outlier: chương ngắn bất thường có thể là dấu hiệu bỏ sót; chương dài bất thường có thể là lặp hoặc AI thêm diễn giải.


## Cách chấm điểm thực dụng

Không nên chấm kiểu “8,7/10” thuần cảm tính. Hãy dùng **error ledger** theo segment, gồm: `Book > Chapter > Segment ID > Source > Target > Category > Subcategory > Severity > Risk > Evidence > Suggested fix > Owner > Status`.

### Severity đề xuất

| Mức lỗi | Ý nghĩa trong sách | Điểm phạt gợi ý | Ví dụ |
| :-- | :-- | --: | :-- |
| Critical | Làm hiểu sai cốt truyện, gây rủi ro pháp lý/đạo đức, hoặc làm hỏng file xuất bản | 25 | Đảo hung thủ–nạn nhân; mất cả đoạn then chốt; nhầm giới tính/quan hệ trọng yếu xuyên truyện |
| Major | Làm sai nghĩa rõ, vỡ logic hoặc phá trải nghiệm đọc đáng kể | 5 | Sai cảnh giới, sai xưng hô trọng yếu, bỏ mệnh đề điều kiện, đổi sắc thái đe dọa thành đùa cợt |
| Minor | Lỗi thật nhưng độc giả vẫn hiểu đúng mạch chính | 1 | Dấu phẩy, từ chưa tự nhiên, biến thể thuật ngữ ít quan trọng |
| Cosmetic | Không sai nghĩa, chỉ cần polish theo style guide | 0–0,25 | Nhịp câu, lựa chọn từ chưa đẹp, lặp từ nhẹ |

Có thể tính:

$$
\text{Weighted Error Rate} =
\frac{25C + 5M + 1m + 0.25c}{\text{số từ đích}} \times 1.000
$$

Tuy nhiên, với văn học, **điểm tổng không được che lỗi chặn phát hành**. Cần có các rule cứng:

- Có bất kỳ lỗi Critical nào: **Fail**, không phụ thuộc điểm.
- Thuật ngữ/xưng hô lõi sai lặp lại: **Fail consistency gate**.
- EPUB lỗi cấu trúc, mất chapter hoặc link mục lục: **Fail technical gate**.
- Điểm thấp nhưng chất văn không đạt rubric tối thiểu: chuyển sang vòng hậu biên tập, không xuất bản.


## Quy trình audit đề xuất

### Giai đoạn 0: Khóa chuẩn đầu vào

Trước khi dịch, lập đầy đủ:

- Brief: thể loại, độc giả, mức trau chuốt, deadline, mục tiêu xuất bản.
- Editorial policy và style guide tiếng Việt.
- Glossary có version, danh sách forbidden variants và quy tắc ưu tiên.
- Character/relationship bible.
- Quy tắc chú thích, tên riêng, xưng hô, đơn vị đo, thơ/câu đối.
- Cấu trúc chuẩn của EPUB/chapter và các chuỗi không được phép dịch.

Đây là phần quyết định lớn nhất. Audit tốt không thể cứu được một pipeline không có chuẩn đích.

### Giai đoạn 1: Pre-flight tự động toàn sách

Chạy toàn bộ trước khi reviewer đọc:

- Extract HTML/EPUB thành segment có ID ổn định.
- So sánh source–target theo số chapter, heading, paragraph, token/word count.
- Quét untranslated, duplicate, missing segment, placeholder/tag mismatch.
- Match glossary và dò forbidden variants.
- Dò tên riêng/quan hệ/xưng hô theo dữ liệu chuẩn.
- Dò số, ngày, đơn vị, tiền, ký hiệu, dấu ngoặc, URL, footnote marker.
- Phát hiện lặp câu, lặp đoạn, chunk overlap và outlier độ dài.

Các lỗi khách quan này phải được sửa trước khi dùng AI audit ngữ nghĩa; nếu không reviewer sẽ lãng phí token vào những lỗi máy có thể bắt chắc chắn.

### Giai đoạn 2: Audit rủi ro bằng AI

Không nhất thiết gửi toàn bộ sách cho model mạnh nhất. Hãy ưu tiên audit sâu các đoạn có risk score cao:

- Chương mở đầu, kết thúc, cao trào, plot twist.
- Cảnh điều tra, chiến đấu, đàm phán, mô tả cơ chế/cảnh giới.
- Đoạn nhiều nhân vật hoặc thoại dày.
- Đoạn có thơ, điển tích, văn ngôn, thành ngữ, lời nói nước đôi.
- Những segment bị glossary checker báo lệch.
- Các chapter có tỷ lệ độ dài nguồn–đích bất thường.
- Các đoạn model dịch có confidence thấp hoặc các reviewer AI bất đồng.

Output của auditor phải là JSON/bảng có bằng chứng nguồn–đích, không cho phép nhận xét mơ hồ kiểu “có vẻ chưa tự nhiên”.

### Giai đoạn 3: Chấm chất văn độc lập

Dùng bản tiếng Việt **không kèm nguyên tác** để kiểm:

- Mạch đọc liền trang.
- Logic có bị đứt không.
- Tên/đại từ có gây nhầm lẫn không.
- Mức “dịch giả hiện diện” hoặc “văn máy” có cao không.
- Nhịp, giọng và cảm xúc có hợp thể loại không.
- Có đoạn nào cần rewrite dù không sai nghĩa không.

Đây là nơi tách hai loại công việc vốn hay bị lẫn: **translation QA** (đúng) và **literary editing** (hay).

### Giai đoạn 4: Human spot-check và hiệu chuẩn

ISO 5060 nhấn mạnh đánh giá phân tích bằng loại lỗi và điểm phạt, đồng thời đề cập vai trò của lấy mẫu và năng lực người đánh giá. Với sách, nên dùng lấy mẫu có rủi ro thay vì ngẫu nhiên hoàn toàn:[^1_6][^1_2]

- 10–20% segment chọn theo risk-based sampling cho bản đã ổn.
- 100% cho chương đầu, chương kết, cảnh then chốt và phần có lỗi hệ thống.
- 2–3% lấy mẫu ngẫu nhiên để tránh “blind spot” của luật/risk model.
- Khi tìm thấy lỗi lặp theo pattern, mở rộng kiểm tra toàn corpus thay vì sửa từng điểm đơn lẻ.

Sau mỗi vòng, cập nhật glossary, rule, prompt và test set. Mục tiêu không chỉ là sửa cuốn hiện tại mà là giảm lỗi ở cuốn sau.

## Dashboard nên có

Với kỹ năng Sheets/Apps Script/Power BI của anh/chị, tôi sẽ không làm một bảng tổng hợp tĩnh mà làm dashboard gồm bốn cấp:

- **Book release gate:** Pass/Conditional Pass/Fail; số lỗi Critical/Major; trạng thái EPUB; checklist pháp lý–metadata.
- **Chapter heatmap:** lỗi trên 1.000 từ theo chương, tách Accuracy, Consistency, Style, Technical.
- **Root-cause dashboard:** lỗi do prompt, glossary thiếu, source khó, segment split, model hallucination, post-edit chưa đủ.
- **Terminology \& entity dashboard:** top thuật ngữ sai, biến thể, nhân vật bị sai xưng hô, lỗi lặp theo translator/model/chapter.
- **Editorial quality dashboard:** điểm tự nhiên, giọng thể loại, độ lặp, dialogue quality, mức can thiệp biên tập.
- **CAPA tracker:** lỗi → nguyên nhân gốc → corrective action → preventive action → rule/prompt/glossary version đã cập nhật.

Một chỉ số rất đáng theo dõi là **escape rate**: tỷ lệ lỗi bị lọt qua Gate tự động và AI QA nhưng bị human reviewer phát hiện. Nó đo chất lượng hệ thống audit thực tế tốt hơn chỉ nhìn tổng số lỗi.

## Khuyến nghị khởi đầu

Tôi khuyên không nên khởi động bằng 100+ tiêu chí chi tiết, dù MQM có hệ phân loại rất rộng. Trong triển khai thực tế, người ta thường chọn một tập con khoảng 20–40 loại lỗi phù hợp với bối cảnh; với dịch sách Việt hóa, nên có taxonomy riêng cho fiction thay vì bê nguyên framework dịch tài liệu kỹ thuật.[^1_7][^1_8]

Bản MVP tốt có thể gồm 8 nhóm:

1. Accuracy: sai dịch, bỏ sót, thêm ý, không dịch.
2. Entities \& facts: tên riêng, số liệu, quan hệ, timeline.
3. Terminology: glossary, cảnh giới/hệ thống, biến thể cấm.
4. Address \& dialogue: xưng hô, người nói, giọng nhân vật.
5. Vietnamese fluency: ngữ pháp, dấu câu, collocation, lặp từ.
6. Literary style: tự nhiên, register, nhịp, sắc thái, thể loại.
7. Culture \& notes: điển cố, chú thích, bản địa hóa nhất quán.
8. EPUB integrity: cấu trúc, HTML, mục lục, metadata, chunk loss/duplication.

Sau 2–3 cuốn, hãy dùng dữ liệu lỗi thực tế để tinh chỉnh trọng số và thêm subcategory. Một hệ thống audit trưởng thành phải “học từ lỗi tái diễn” của chính pipeline, chứ không chỉ ngày càng dài hơn về checklist.

<span style="display:none">[^1_10][^1_11][^1_12][^1_13][^1_14][^1_15][^1_16][^1_17][^1_18][^1_19][^1_20][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: image.jpg

[^1_2]: https://standards.iteh.ai/catalog/standards/iso/48dc14ee-cffc-4c0b-b184-b1707ac6e65e/iso-5060-2024

[^1_3]: https://themqm.org/error-types-2/typology/

[^1_4]: https://www.jostrans.soap2.ch/issue23/art_melby.pdf

[^1_5]: https://slator.com/new-iso-standard-5060-focuses-on-human-evaluation-to-ensure-translation-quality/

[^1_6]: https://standards.iteh.ai/catalog/standards/sist/3969698e-05eb-4ce6-bc67-6d2d81a6eb40/sist-iso-5060-2024

[^1_7]: https://www.themqm.org/mqm-pillars/the-mqm-scoring-models/

[^1_8]: https://kt.tc/en/blog/mqm-complete-guide

[^1_9]: https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=6592\&context=etd

[^1_10]: https://cdn.standards.iteh.ai/sist-preview/80701/38f1b065860a4ae6bc5f1ceddd5063ad/SIST-ISO-5060-2024.pdf

[^1_11]: https://cdn.standards.iteh.ai/samples/80701/38f1b065860a4ae6bc5f1ceddd5063ad/SIST-ISO-5060-2024.pdf

[^1_12]: https://cdn.standards.iteh.ai/samples/80701/d59c6554109d4f59b9a6b9818cff2c54/ISO-5060-2024.pdf

[^1_13]: https://community.translatorswb.org/t/dqf-mqm-error-typology/10827/1

[^1_14]: https://languagemiscellany.com/2024/03/isos-on-translation/

[^1_15]: https://snapintel.io/blog/mqm-vs-lisa-qa-model-which-translation-quality-framework-should-you-use

[^1_16]: https://atccertification.com/iso-5060-evaluation-of-translation-output/

[^1_17]: interests.ai_translation

[^1_18]: preferences.prompt_customization.translation_workflow

[^1_19]: interests.ai_tools.antigravity.long_term_memory

[^1_20]: projects.ai_translation_sales


---

# xây dựng cho tôi hệ thống này một cách toàn diện với các input như sau:

- File epub đã được dịch tiếng Việt hoàn chỉnh. File gốc nằm ở folder mẹ cao hơn 1 bậc
- Model Gemini Flash (latest)
- Cần tách nhỏ theo phần/chương/đoạn để dịch
- Hoàn thiện tool audit ở mức đô production ready (không MVP) một cách phổ quát, AI sẽ xác định cần audit như thế nào.

Bắt đầu plan và thực hiện.

Tôi có thể thiết kế và bắt đầu triển khai hệ thống audit production-ready này, nhưng hiện chưa truy xuất được hai EPUB từ Google Drive: tìm kiếm Drive trả về lỗi và không có file nào được staging vào workspace.[^2_1]

Để **thực hiện audit thật** trên sách của anh/chị, hãy tải lên trực tiếp EPUB bản dịch tiếng Việt; hoặc gửi link/thư mục Drive có quyền truy cập rõ ràng và tên file. Khi có file, tôi sẽ bắt đầu bằng bước extract/đối chiếu cấu trúc, tìm EPUB gốc ở thư mục mẹ, tạo manifest song ngữ và chạy các gate tự động trước.

## Phạm vi hệ thống

Tôi đề xuất xây hệ thống với tên làm việc **EpubTranslateAudit**: một pipeline audit song ngữ, bảo toàn EPUB, thiết kế cho sách dài và có thể chạy theo batch. “AI tự xác định cần audit gì” sẽ được thực hiện theo mô hình **adaptive audit orchestration**:

1. Hệ thống trích xuất, phân đoạn và lập bản đồ giữa EPUB gốc và EPUB Việt.
2. Rule engine chạy toàn bộ corpus để phát hiện lỗi khách quan.
3. AI profiler đọc metadata, mục lục, một mẫu đại diện, và các kết quả rule-based để suy luận loại sách, phong cách, mức rủi ro và rubric nên ưu tiên.
4. AI planner tự tạo `Audit Plan` cho đúng cuốn sách: độ sâu audit, nhóm tiêu chí, chiến lược lấy mẫu, phân bổ token và ngưỡng phát hành.
5. Gemini Flash audit theo segment/chunk với source, target, context, glossary và rule findings.
6. AI adjudicator hợp nhất lỗi, giảm false positive, phát hiện lỗi hệ thống và sinh corrective/preventive actions.
7. Hệ thống tạo báo cáo, issue ledger, dashboard data và EPUB đã kiểm tra kỹ thuật.

Khung error taxonomy sẽ dựa trên cách tiếp cận đánh giá phân tích bằng loại lỗi và điểm phạt của ISO 5060, kết hợp MQM nhưng mở rộng mạnh cho tiểu thuyết, xưng hô, tính liên tục truyện, văn phong Việt và integrity EPUB.[^2_2][^2_3]

## Kiến trúc production-ready

```text
INPUT/
├── translated_vi.epub
├── ../source_original.epub
├── project_config.yaml
├── glossary/
│   ├── terminology.csv
│   ├── entities.json
│   ├── characters.json
│   ├── relationships.json
│   ├── style_guide.md
│   └── editorial_policy.md
└── overrides/
    ├── accepted_exceptions.json
    └── manual_alignment.csv

PIPELINE/
├── 01_ingest/
│   ├── unpack EPUB
│   ├── validate ZIP/OPF/nav/NCX
│   ├── extract metadata, HTML, CSS, media
│   └── fingerprint source and target
├── 02_segment/
│   ├── identify part/chapter/section
│   ├── preserve XHTML hierarchy
│   ├── split paragraphs into audit segments
│   ├── retain stable anchors and offsets
│   └── build source-target alignment
├── 03_static_qa/
│   ├── completeness
│   ├── structural integrity
│   ├── tag/placeholder integrity
│   ├── numbers/dates/units
│   ├── untranslated text
│   ├── duplication
│   ├── glossary/entity consistency
│   └── terminology forbidden variants
├── 04_adaptive_planner/
│   ├── genre/style profiler
│   ├── risk scorer
│   ├── audit scope planner
│   ├── sampling planner
│   └── budget and priority allocator
├── 05_ai_audit/
│   ├── bilingual semantic auditor
│   ├── Vietnamese literary editor
│   ├── dialogue/address auditor
│   ├── continuity and entity auditor
│   ├── cultural/localization auditor
│   └── technical evidence verifier
├── 06_adjudication/
│   ├── schema validation
│   ├── evidence check
│   ├── duplicate clustering
│   ├── severity calibration
│   ├── root-cause analysis
│   └── release-gate decision
├── 07_reporting/
│   ├── HTML report
│   ├── CSV/XLSX issue ledger
│   ├── JSON audit package
│   ├── Power BI-ready tables
│   ├── CAPA log
│   └── machine-readable release manifest
└── 08_outputs/
    ├── audited_epub/
    ├── reports/
    ├── audit_data/
    ├── logs/
    └── review_queue/
```


## Các thành phần cần xây

### 1. EPUB ingestion và structural integrity

Module này là gate bắt buộc, không dùng AI để thay thế parser.

Nó sẽ:

- Giải nén EPUB vào workspace tạm và kiểm tra cấu trúc container.
- Đọc `META-INF/container.xml`, OPF package document, spine, manifest, `nav.xhtml`, NCX nếu có.
- Xác định thứ tự đọc thật theo `spine`, không dựa đơn thuần vào tên file.
- Phân loại nội dung: front matter, part, chapter, section, footnote/endnote, appendix, afterword, TOC.
- Giữ nguyên đường dẫn file, `id`, `href`, anchor, class, CSS và liên kết nội bộ.
- Tạo checksum SHA-256 cho EPUB, XHTML, CSS, media và từng segment.
- Báo lỗi ngay nếu bản dịch mất chương, trùng chương, sai thứ tự đọc, hỏng liên kết, mất hình/bảng, mất chú thích hoặc sai metadata.

**Nguyên tắc:** audit nội dung không được làm thay đổi EPUB đầu vào. Nếu có tính năng sửa tự động sau này, nó phải tạo bản EPUB mới, lưu diff, checkpoint và rollback đầy đủ.

### 2. Segmenter theo phần/chương/đoạn

Anh/chị yêu cầu tách nhỏ theo phần/chương/đoạn; hệ thống sẽ tách theo bốn cấp thay vì chỉ chunk token:


| Cấp | Đơn vị | Vai trò audit |
| :-- | :-- | :-- |
| Book | Một EPUB hoàn chỉnh | Metadata, style profile, glossary, release decision |
| Part | Quyển/phần/tập | Giữ bối cảnh lớn, đổi ngôi kể hoặc đổi tuyến truyện |
| Chapter | Chương | Audit logic, nhân vật, diễn tiến và consistency theo chương |
| Block | Heading, paragraph, quote, note, table cell, verse | Đơn vị mapping XHTML và kiểm lỗi cấu trúc |
| Segment | 1–3 câu hoặc đoạn nhỏ giới hạn token | Đơn vị gửi Gemini để audit song ngữ |

Mỗi segment cần có ID ổn định, ví dụ:

```text
book_id=novel_001
part_id=part_02
chapter_id=ch_031
xhtml_path=Text/chapter_031.xhtml
block_id=p_018
segment_id=ch_031.p_018.s_002
source_hash=...
target_hash=...
prev_segment_id=...
next_segment_id=...
```

Không được cắt tùy tiện giữa:

- Lời thoại và attribution của người nói.
- Câu có đại từ hồi chỉ hoặc ellipsis.
- Danh sách, thơ, câu đối, thư từ, tin nhắn.
- Chú thích neo vào câu.

```
- HTML inline như `<em>`, `<strong>`, `<ruby>`, hyperlink.
```

- Bảng hoặc đoạn có cấu trúc đặc biệt.

Với Gemini Flash, mỗi request audit nên mang một “audit packet” gồm segment mục tiêu, 1–2 segment trước/sau, context chương nén, entity liên quan và rule findings. Điều này giúp giảm lỗi do audit từng đoạn vô ngữ cảnh.

### 3. Alignment nguồn–đích

Đây là phần quan trọng nhất nếu source và target EPUB không có cấu trúc giống hệt.

Pipeline alignment gồm:

1. **Document-level mapping:** map spine/source HTML với spine/target HTML.
2. **Chapter-level matching:** dựa vào tiêu đề, thứ tự, độ dài, tên file, heading hierarchy.
3. **Block-level alignment:** heading/paragraph/quote/note/table.
4. **Sentence/segment alignment:** dùng thuật toán kết hợp độ dài, dấu câu, số, named entity, heading and anchor.
5. **Low-confidence queue:** mọi mapping dưới ngưỡng phải đánh dấu để AI alignment reviewer xem lại hoặc người dùng override.

Mỗi cặp mapping cần có:

```json
{
  "alignment_id": "src_ch031_p018__vi_ch031_p018",
  "source_segment_ids": ["src.ch031.p018.s01", "src.ch031.p018.s02"],
  "target_segment_ids": ["vi.ch031.p018.s01"],
  "alignment_type": "many_to_one",
  "confidence": 0.94,
  "method": ["structure", "length_ratio", "anchor", "ai_verified"],
  "review_required": false
}
```

Hệ thống phải chấp nhận quan hệ một–nhiều hoặc nhiều–một vì bản dịch tiếng Việt có thể tách/gộp câu hợp lý. Cần phân biệt trường hợp đó với lỗi mất hoặc thêm nội dung.

### 4. Rule-based quality gates

Các luật dưới đây chạy **100% toàn sách**, chi phí thấp và có bằng chứng rõ ràng.


| Gate | Kiểm tra | Hành động |
| :-- | :-- | :-- |
| EPUB validity | ZIP/container/OPF/spine/manifest/nav/NCX hợp lệ | Critical nếu không mở/đọc được |
| Structure parity | Part/chapter/heading/note/table/image không bị mất, lặp hoặc đảo thứ tự | Critical hoặc Major |
| Text completeness | Không còn đoạn nguồn, đoạn rỗng, đoạn bị bỏ hoặc duplicate | Critical/Major |
| Markup fidelity | HTML tags, link, anchor, footnote, emphasis, placeholder được giữ | Major/Critical tùy ảnh hưởng |
| Numeric fidelity | Số, phần trăm, ngày, giờ, tiền, cấp bậc, đơn vị, ký hiệu | Major nếu làm sai nghĩa |
| Entity integrity | Tên riêng, địa danh, tổ chức, vật phẩm, chức danh, alias | Major nếu sai hệ thống |
| Glossary compliance | Thuật ngữ chuẩn, biến thể cấm, lần xuất hiện cần chú thích | Minor đến Major |
| Dialogue QA | Dấu thoại, quote, attribution, speaker tags | Minor/Major |
| Language residue | Ký tự lạ, OCR noise, text nguồn, placeholder, encoding error | Major |
| Repetition QA | Câu/đoạn lặp bất thường, chunk overlap, boilerplate hallucination | Major |
| Length outlier | Chênh lệch source–target bất thường theo chapter/block | Cờ rủi ro, không tự kết luận |
| Style lint | Lặp từ, câu dịch máy, hạt từ thừa, dấu câu, space, typography | Minor/Cosmetic |

### 5. Adaptive Audit Planner

Đây là cơ chế để AI “xác định cần audit như thế nào”, nhưng vẫn chịu kiểm soát bằng rule và policy.

Planner không được quyền tự bỏ qua các gate bắt buộc. Nó chỉ được quyết định:

- Loại audit cần tăng cường.
- Nhóm segment nào cần kiểm 100%.
- Sampling rate với khu vực rủi ro thấp.
- Context window cần cấp cho từng loại đoạn.
- Rubric chuyên ngành theo thể loại.
- Trọng số severity và ngưỡng release đề xuất.
- Reviewer nào được gọi trước hoặc cần gọi thêm.

Ví dụ:


| Dấu hiệu AI phát hiện | Audit tăng cường |
| :-- | :-- |
| Trinh thám, mystery, courtroom | Logic, timeline, evidence chain, pronoun/reference, spoiler |
| Tiên hiệp/huyền huyễn | Cảnh giới, công pháp, danh xưng, phe phái, thuật ngữ hệ thống |
| Cổ đại/lịch sử | Tước vị, niên hiệu, lễ nghi, điển cố, register cổ phong |
| Romance/BL/GL | Xưng hô, sắc thái thân mật, consent, subtext, character voice |
| Kinh dị/tâm lý | Nhịp, ambiguity, unreliable narrator, hình ảnh và tension |
| Sci-fi/fantasy | Worldbuilding, units, invented term, continuity, causal logic |
| Phi hư cấu/học thuật | Fact, trích dẫn, bảng, chú thích, thuật ngữ kỹ thuật |
| Sách kỹ năng/business | Khái niệm, ví dụ, số liệu, actionability, tone chuyên nghiệp |

Output của module này là file `audit_plan.json`, ví dụ:

```json
{
  "book_profile": {
    "primary_genre": "historical_mystery",
    "secondary_genres": ["political_intrigue"],
    "narration": "third_person_limited",
    "style_register": "semi_classical_vietnamese",
    "confidence": 0.89
  },
  "scope": {
    "static_rules": "100_percent",
    "semantic_audit": "100_percent_high_risk_and_35_percent_baseline",
    "literary_style_audit": "100_percent_dialogue_and_25_percent_narration",
    "continuity_audit": "100_percent_entities_and_plot_markers"
  },
  "priority_dimensions": [
    "accuracy",
    "entity_consistency",
    "timeline_logic",
    "dialogue_and_address",
    "register_and_literary_style"
  ],
  "release_gates": {
    "critical_errors_allowed": 0,
    "major_errors_per_1000_words_max": 0.3,
    "glossary_compliance_min": 0.985,
    "unresolved_alignment_allowed": 0
  }
}
```


### 6. Gemini Flash review agents

Gemini Flash phù hợp cho chạy số lượng lớn, nhưng để đạt production-ready, hệ thống phải dùng structured output, retry, validation và adjudication thay vì tin vào nhận xét văn xuôi.

Các agent logic gồm:


| Agent | Nhiệm vụ | Đầu ra |
| :-- | :-- | :-- |
| Book Profiler | Nhận diện thể loại, giọng, rủi ro, yêu cầu audit | `book_profile.json` |
| Alignment Reviewer | Xác minh cặp source–target không chắc chắn | alignment decision |
| Semantic Auditor | Kiểm sai dịch, bỏ sót, thêm ý, sai logic | issue records có evidence |
| Consistency Auditor | Entity, thuật ngữ, xưng hô, timeline, relationship | issue records + glossary proposals |
| Literary Editor | Độ mượt Việt, register, nhịp, lời thoại, voice | issue records không tự rewrite toàn đoạn |
| Localization Auditor | Điển cố, chú thích, đơn vị, tên riêng, văn hóa | issue records + policy conflict |
| Technical Auditor | Xác minh lỗi markup, note, link và cấu trúc được rule cờ | evidence verification |
| Adjudicator | Khử trùng, hiệu chuẩn severity, chống hallucination | final issue ledger |
| Root-cause Agent | Gom nhóm pattern lỗi, sinh CAPA | root cause + prevention rules |
| Release Gate Agent | Ra Pass/Conditional Pass/Fail theo policy | signed release decision |

Mỗi agent trả về JSON theo schema cố định. Ví dụ cho một issue:

```json
{
  "issue_id": "AQ-CH031-P018-S02-001",
  "category": "accuracy",
  "subcategory": "mistranslation",
  "severity": "major",
  "confidence": 0.93,
  "source_evidence": "Original text excerpt here",
  "target_evidence": "Vietnamese target excerpt here",
  "explanation_vi": "Bản dịch đảo quan hệ nguyên nhân–kết quả...",
  "impact_vi": "Làm sai động cơ của nhân vật trong cảnh điều tra.",
  "suggested_correction_vi": "Đề nghị sửa theo hướng...",
  "requires_human_review": true,
  "reproducible_rule_id": null,
  "segment_id": "vi.ch031.p018.s002",
  "context_segment_ids": [
    "vi.ch031.p018.s001",
    "vi.ch031.p018.s003"
  ]
}
```

Không cho phép Gemini trả về các lỗi không có `source_evidence`, `target_evidence`, category và severity. Mọi JSON không hợp schema phải retry có kiểm soát hoặc chuyển sang queue.

## Các release gate

### Gate A: Technical blocking

Phải đạt tất cả:

- EPUB mở được bằng validator và engine đọc mục tiêu.
- Không mất/nhân đôi chapter, segment, note, anchor, image hoặc spine item.
- Không có `unresolved_alignment`.
- Không còn source residue hoặc encoding corruption.
- Không có HTML/OPF/navigation critical error.


### Gate B: Accuracy blocking

- `Critical = 0`.
- Không còn lỗi Major chưa giải quyết trong phần plot-critical.
- Không có lỗi sai người nói, quan hệ nhân vật, hung thủ–nạn nhân, phủ định, số liệu hoặc timeline ở mức ảnh hưởng cốt truyện.
- Không có missing/added content không được phê duyệt.


### Gate C: Consistency blocking

- Glossary compliance đạt ngưỡng theo policy, gợi ý tối thiểu 98,5%.
- Entity core consistency đạt 100% cho các thực thể khóa.
- Xưng hô core relation không còn mâu thuẫn.
- Không còn term drift theo chương hoặc theo part.


### Gate D: Literary acceptance

- Vietnamese readability đạt ngưỡng đã định.
- Register không bị drift lớn.
- Dialogue sample đạt chuẩn tự nhiên.
- Các lỗi style còn lại chỉ được ở mức cosmetic/minor và trong error budget.


### Gate E: Human acceptance

Dù hệ thống production-ready, bản phát hành thương mại vẫn nên có human sign-off ở ít nhất:

- Chapter đầu.
- Chapter kết.
- Tất cả chapter high-risk.
- Toàn bộ lỗi Major/critical đã sửa.
- Một mẫu ngẫu nhiên độc lập sau khi sửa.


## Cấu trúc dữ liệu đầu ra

Để tích hợp tốt với Google Sheets, BigQuery hoặc Power BI, tôi đề xuất sinh các bảng độc lập:

```text
audit_run
book
epub_file
chapter
segment
alignment
rule_finding
ai_finding
issue
issue_cluster
issue_resolution
glossary_term
entity
entity_occurrence
risk_score
audit_plan
release_gate
capa_action
model_run
token_usage
processing_log
```

Các bảng quan trọng nhất:

- `segments.csv`: source–target aligned segments, hashes, chapter, block, context.
- `issues.csv`: toàn bộ lỗi sau adjudication.
- `issue_clusters.csv`: lỗi lặp có cùng nguyên nhân.
- `risk_scores.csv`: vì sao một segment/chapter được audit sâu.
- `glossary_compliance.csv`: term chuẩn, occurrences, violations.
- `release_report.json`: tình trạng gate có thể máy đọc.
- `capa.csv`: corrective action, preventive action, owner, status.
- `dashboard_fact_issues.csv`: bảng fact cho Power BI.
- `dashboard_dim_*`: dimensions cho book/chapter/category/severity/model/run.


## Công nghệ đề xuất

Để dễ triển khai local, có thể chạy Windows, tích hợp Claude Code/Antigravity và phù hợp workflow hiện tại của anh/chị:


| Thành phần | Đề xuất |
| :-- | :-- |
| Runtime | Python 3.12 |
| CLI | Typer hoặc Click |
| Config | YAML + Pydantic settings |
| EPUB/XML | `ebooklib`, `lxml`, `beautifulsoup4`, `zipfile` |
| Validation | `epubcheck` qua Java subprocess, `lxml` custom validators |
| Alignment | `rapidfuzz`, `sentence-splitter`, Unicode normalization, heuristic + Gemini fallback |
| Storage | SQLite + DuckDB; nâng cấp PostgreSQL khi multi-user |
| Job queue | Prefect hoặc Celery/RQ; local thì Prefect + SQLite |
| LLM | Gemini API, `gemini-*-flash-latest`, structured JSON output |
| Resilience | Tenacity retry, exponential backoff, rate limiter, idempotency keys |
| Observability | Structured JSON logs, OpenTelemetry/Sentry tùy mức triển khai |
| Reporting | Jinja2 HTML, Pandas/XlsxWriter, CSV, JSON |
| Dashboard | Power BI đọc DuckDB/CSV hoặc dataflow |
| UI tùy chọn | Streamlit/FastAPI + React sau khi CLI ổn định |
| Test | Pytest, golden EPUB fixtures, schema tests, regression corpus |

## Kế hoạch thực hiện

### Phase 1 — Foundation

- Chốt cấu trúc thư mục và file config dự án.
- Xây EPUB parser, validator, extractor.
- Xây manifest toàn sách và stable segment ID.
- Xây source–target alignment có confidence score.
- Thiết kế SQLite schema, event log, run manifest.
- Tạo bộ golden test: EPUB hợp lệ, EPUB lỗi, chương mất, text lặp, footnote lỗi, mapping 1–nhiều.

**Done khi:** có thể nạp hai EPUB và xuất được `book_manifest.json`, `segments.csv`, `alignment.csv`, `technical_findings.csv`.

### Phase 2 — Deterministic QA

- Hoàn thiện 100% static gates.
- Glossary/entity engine.
- Quét xưng hô, text source còn sót, số liệu, trùng lặp, outlier.
- Sinh error ledger theo schema.
- Tạo release gate kỹ thuật.

**Done khi:** mọi lỗi cấu trúc hoặc completeness cứng đều xuất được bằng chứng tái lập.

### Phase 3 — Gemini adaptive audit

- Tạo profile prompt và audit-plan prompt.
- Tạo JSON schemas và response validator.
- Tạo semantic, consistency, literary, localization agents.
- Tạo rate limit, retry, cache, checkpoint/resume.
- Tạo confidence, risk score, sampling và context-pack builder.

**Done khi:** có thể audit một ebook dài theo batch, dừng/chạy lại không mất trạng thái, không audit trùng segment và không hỏng dữ liệu.

### Phase 4 — Adjudication và CAPA

- Gộp duplicate findings.
- Chặn findings không đủ evidence.
- Hiệu chuẩn severity và score.
- Tìm root cause theo model/chapter/term/prompt/rule.
- Sinh đề xuất cập nhật glossary, policy và prompt.
- Lập danh sách sửa theo ưu tiên: Critical → Major plot-critical → systemic → Minor.

**Done khi:** báo cáo không chỉ “có lỗi” mà chỉ rõ lỗi gì, ở đâu, bằng chứng nào, sửa thế nào và ngăn lặp ra sao.

### Phase 5 — Reporting, dashboard, vận hành

- HTML report dễ đọc.
- XLSX issue ledger có filter, freeze pane, màu theo severity.
- Bộ CSV star-schema cho Power BI.
- Audit history, so sánh run trước/sau.
- Release manifest có checksum và versioning.
- UI review queue tùy chọn.
- CI/CD, test corpus, documentation, security checklist.

**Done khi:** có thể dùng lặp lại cho nhiều sách và theo dõi chất lượng pipeline qua thời gian.

## Cần file để bắt đầu chạy

Vui lòng cung cấp một trong hai cách sau:

1. **Tải trực tiếp hai file EPUB**: bản gốc và bản dịch tiếng Việt; đây là cách chắc chắn nhất để tôi bắt đầu ingest, alignment và audit thực tế.
2. **Gửi đường dẫn Google Drive và tên file cụ thể**, đồng thời kiểm tra quyền truy cập connector. Lần tìm kiếm vừa rồi không thể lấy được dữ liệu từ Drive do lỗi nguồn kết nối, nên hiện chưa thể tự tìm file trong “folder mẹ cao hơn một bậc”.[^2_1]

Khi có hai file, tôi sẽ bắt đầu ngay bằng Phase 1 trên chính cấu trúc EPUB của anh/chị, sau đó xuất bộ manifest, kế hoạch audit tự động và danh sách gate/rule thực tế cho cuốn sách đó.

<div align="center">⁂</div>

[^2_1]: image.jpg

[^2_2]: https://standards.iteh.ai/catalog/standards/iso/48dc14ee-cffc-4c0b-b184-b1707ac6e65e/iso-5060-2024

[^2_3]: https://themqm.org/error-types-2/typology/


---

# xây dựng cho tôi tool/repo phổ quát (gồm các file cần thiết scripts,prompts, agents/skills...), không cần epub thực tế trong giai đoạn này, user tải về và paste path epub folder để audit

Tôi đã tạo một blueprint/repository hoàn chỉnh cho **EpubTranslateAudit**: một tool audit song ngữ EPUB theo hướng production-ready, có CLI để người dùng paste đường dẫn EPUB bản dịch, tự tìm EPUB gốc ở folder mẹ hoặc nhận `--source` rõ ràng, dùng Gemini Flash qua structured JSON, có rule engine, agent prompts, release gate, cache/resume, issue ledger và dữ liệu sẵn cho Power BI.

Tôi chưa thể “cài code trực tiếp” thành một repository Git đầy đủ nhiều file trong một thao tác duy nhất ở đây, nhưng tài liệu đã cung cấp đầy đủ cấu trúc repo, nội dung cấu hình, prompt, schema, code skeleton và thứ tự triển khai để đưa vào Antigravity/Claude Code/Cursor triển khai thành project thực. File blueprint đã được tạo ở phần file đính kèm: **EpubTranslateAudit repository blueprint**.

## Điểm thiết kế cốt lõi

Tool này không coi AI là người chấm duy nhất. Nó vận hành theo thứ tự:

```text
EPUB source + EPUB Việt
→ validate EPUB
→ extract cấu trúc
→ tách Part/Chapter/Block/Segment
→ alignment source–target
→ static QA 100%
→ AI profile thể loại/rủi ro
→ AI tạo audit plan
→ Gemini audit theo packet có context
→ adjudication/deduplication
→ release gates
→ HTML/XLSX/CSV/Power BI/CAPA
```

Các gate kỹ thuật, đầy đủ nội dung, markup, số liệu, glossary và alignment sẽ chạy 100% bằng code. AI chỉ được quyền tăng độ sâu audit, ưu tiên rủi ro và đề xuất các chiều kiểm tra theo thể loại; AI không được tự bỏ qua bất kỳ gate bắt buộc nào.

Việc dùng structured output thay vì để Gemini trả lời tự do là bắt buộc: Gemini API hỗ trợ JSON Schema/Pydantic để tạo đầu ra có cấu trúc, giúp validate và xử lý issue ledger đáng tin cậy hơn. Tool cũng cần ghi nhận model thực tế được resolve tại thời điểm chạy vì alias `latest` có thể được Google cập nhật sang bản phát hành mới.[^3_1][^3_2][^3_3]

## Cách người dùng chạy tool

Workflow tối giản theo đúng yêu cầu “paste path EPUB folder để audit”:

```powershell
epub-audit run `
  --translated "D:\Books\Project\vi\book_vi.epub" `
  --output "D:\Books\Project\audit-output"
```

Theo mặc định, tool sẽ tìm source EPUB theo thứ tự an toàn:

1. Có `--source` thì dùng source đó.
2. Có `source_epub` trong file config thì dùng file đó.
3. Tìm một EPUB duy nhất khác bản dịch trong folder mẹ.
4. Nếu có hơn một ứng viên, **dừng và yêu cầu chọn**, không đoán bừa.
5. Chỉ mở rộng tìm ở folder mẹ cao hơn nữa nếu người dùng bật rõ `allow_grandparent_discovery`.

Khi muốn chỉ định cụ thể:

```powershell
epub-audit run `
  --translated "D:\Books\Project\vi\book_vi.epub" `
  --source "D:\Books\Project\book_original.epub" `
  --glossary "D:\Books\Project\knowledge\glossary.csv" `
  --entities "D:\Books\Project\knowledge\entities.json" `
  --style-guide "D:\Books\Project\knowledge\style_guide.md" `
  --output "D:\Books\Project\audit-output" `
  --resume
```


## Thành phần production-ready

Blueprint bao gồm:

- Cấu trúc `src/`, `tests/`, `configs/`, `prompts/`, `scripts/`, `docs/`, `outputs/`.
- Python CLI dùng Typer.
- Parser EPUB, extractor XHTML, chapter detector, segmenter và source–target aligner.
- Tích hợp EPUBCheck; EPUBCheck có thể xuất kết quả validation dưới dạng JSON bằng tham số `--json`, thuận tiện để đưa vào rule engine và dashboard.[^3_4]
- Rule engine cho: EPUB integrity, missing/duplicate text, untranslated residue, markup, navigation, footnotes, số liệu, glossary, entities, xưng hô, dialogue, typography, repetition và outlier độ dài.
- Gemini client có Pydantic schema, JSON validation, exponential backoff, cache key, resumability và model configuration.
- Bộ prompts chuyên biệt: Book Profiler, Audit Planner, Semantic Auditor, Consistency Auditor, Literary Auditor, Localization Auditor, Alignment Reviewer, Adjudicator và Root Cause/CAPA.
- Audit taxonomy versioned, severity policy và release decision engine.
- Output: `issue_ledger.xlsx`, HTML report, JSON audit package, CSV star schema cho Power BI, review queue và CAPA log.
- Test strategy: unit, golden tests, schema contract tests, mocked end-to-end tests và regression corpus.


## Output cuối mỗi lần audit

```text
audit-output/
├── run_manifest.json
├── audit_plan.json
├── release_decision.json
├── reports/
│   ├── audit_report.html
│   ├── issue_ledger.xlsx
│   └── executive_summary.md
├── data/
│   ├── segments.csv
│   ├── alignments.csv
│   ├── static_findings.csv
│   ├── issues.csv
│   ├── glossary_compliance.csv
│   ├── risk_scores.csv
│   ├── capa.csv
│   └── powerbi/
└── review_queue/
    ├── alignment_review.csv
    ├── major_critical_review.csv
    └── human_signoff_checklist.md
```

`release_decision.json` phải biểu đạt rõ `PASS`, `CONDITIONAL PASS` hoặc `FAIL`; không được dùng điểm tổng để che một lỗi Critical, chapter bị mất, hay alignment chưa giải quyết.

## Bước triển khai tiếp theo

Để biến blueprint thành repo hoạt động, hãy tạo một folder Git trống rồi giao cho coding agent với chỉ dẫn:

> “Đọc toàn bộ file EpubTranslateAudit repository blueprint. Tạo đúng cấu trúc repository, triển khai theo Implementation Order, ưu tiên Phase 1–2 trước. Không thay đổi input EPUB. Viết test ngay khi tạo module. Khi xong Phase 1–2, chạy test, tạo một public-domain EPUB fixture tối thiểu và báo cáo các lệnh chạy đã xác minh.”

Sau đó triển khai theo 8 phase trong tài liệu, không nên nhảy ngay vào UI. CLI + deterministic rules + alignment + artifact pipeline là nền tảng; UI, dashboard hoặc auto-fix chỉ nên xây sau khi audit artifact và release gate đã ổn định.

<span style="display:none">[^3_10][^3_11][^3_12][^3_13][^3_14][^3_15][^3_5][^3_6][^3_7][^3_8][^3_9]</span>

<div align="center">⁂</div>

[^3_1]: https://ai.google.dev/gemini-api/docs/structured-output

[^3_2]: https://ai.google.dev/gemini-api/docs/generate-content/structured-output

[^3_3]: https://ai.google.dev/gemini-api/docs/models

[^3_4]: https://daisy.github.io/epubcheck-website/docs/user/cli/

[^3_5]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/sdks/overview

[^3_6]: https://ai.google.dev/api/models

[^3_7]: https://ai.google.dev/gemini-api/docs

[^3_8]: https://ai.google.dev/gemini-api/docs/libraries

[^3_9]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/control-generated-output

[^3_10]: https://reference.langchain.com/python/langchain-google-genai/chat_models/ChatGoogleGenerativeAI/response_schema

[^3_11]: https://github.com/googleapis/python-genai

[^3_12]: https://github.com/w3c/epubcheck/wiki

[^3_13]: https://github.com/w3c/epubcheck

[^3_14]: https://deepwiki.com/google-gemini/cookbook/4.4-json-mode-and-structured-output

[^3_15]: https://deepwiki.com/google-gemini/cookbook/4.4-structured-output-and-json-mode


---

# Cách tối ưu cơ chế alignment source target cho file epub lớn

Thiết kế Static QA ruleset cho bản dịch tiếng Việt
Xây dựng release gate tự động chặn bản dịch kém chất lượng
Cấu hình Pydantic schema cho Gemini structured output
tôi dùng chatbox trong vscode để yêu cầu AI thực thi

Nếu anh/chị dùng Chatbox trong VS Code để yêu cầu AI thực thi, cách hiệu quả nhất là **chia việc theo các implementation ticket có tiêu chí nghiệm thu rõ ràng**, thay vì yêu cầu “xây toàn bộ tool”. Dưới đây là thiết kế kỹ thuật có thể copy từng khối vào Chatbox để AI triển khai lần lượt.

Nền tảng cần giữ là: EPUB có `package document` xác định resource và reading order qua `spine`, còn navigation document quản lý TOC/landmark; vì vậy alignment phải bám vào spine/XHTML/anchor trước, tuyệt đối không chỉ dựa vào tên file hay text thuần.[^4_1][^4_2]

## 1. Alignment EPUB lớn

### Nguyên tắc kiến trúc

Không gửi toàn bộ EPUB hay toàn bộ chương vào Gemini để map source–target. Với sách lớn, alignment phải là pipeline nhiều tầng, từ rẻ và chắc chắn đến đắt và thông minh:

```text
EPUB structure alignment
→ chapter alignment
→ block/paragraph alignment
→ sentence/segment alignment
→ low-confidence AI verification
→ human-review queue
```

Tầng sau chỉ xử lý các điểm mà tầng trước không tự tin. Đây là điều kiện để chạy được sách vài trăm chương mà không tiêu tốn API vô kiểm soát.

### Tầng 0: Canonicalization

Trước khi map, convert cả source và target thành dạng chuẩn hóa, nhưng **không sửa file EPUB gốc**.

Mỗi block phải lưu:

```json
{
  "book_id": "book_001",
  "edition": "source",
  "spine_index": 31,
  "xhtml_path": "Text/chapter_031.xhtml",
  "xpath": "/html/body/section/p[^4_18]",
  "block_id": "src.ch031.p018",
  "kind": "paragraph",
  "epub_type": null,
  "text_raw": "Nội dung nguyên bản...",
  "text_normalized": "Nội dung chuẩn hóa...",
  "char_count": 308,
  "word_count": 58,
  "number_tokens": ["15", "3"],
  "entity_candidates": ["Tên A", "Tên B"],
  "text_hash": "sha256..."
}
```

Chuẩn hóa chỉ phục vụ matching:

- Unicode NFC.
- Chuẩn hóa newline, non-breaking space, zero-width space.
- Chuẩn hóa quote/dash/ellipsis thành token nội bộ.
- Bỏ khoảng trắng thừa.
- Tách note marker khỏi nội dung text để tránh làm nhiễu match.
- Giữ lại bản `text_raw`, `xpath`, inline markup và node map để truy vết/sửa sau này.
- Không hạ toàn bộ chữ thường đối với tiếng Việt vì cần giữ entity và title case; nếu cần, tạo thêm field `text_casefolded`.


### Tầng 1: Spine và chapter alignment

Đây là tầng quyết định. Không dùng LLM nếu map được bằng cấu trúc.

Ưu tiên tín hiệu theo thứ tự:

1. `spine_index` và thứ tự reading order.
2. `epub:type`, heading hierarchy (`h1`–`h6`), landmark, `nav.xhtml`.
3. Số chương: `Chương 31`, `Chapter 31`, `第31章`, `卷`, `Phần`, `Part`, `Prologue`, `Epilogue`.
4. Anchor/link map trong mục lục.
5. Tên file XHTML.
6. Độ dài content.
7. Named entity, số chương, ký hiệu chương.
8. AI review nếu vẫn mơ hồ.

Mỗi chapter mapping nên lưu confidence và rationale:

```json
{
  "alignment_id": "chapter.src.031__vi.031",
  "source_chapter_id": "src.ch031",
  "target_chapter_id": "vi.ch031",
  "confidence": 0.995,
  "signals": {
    "spine_order": 1.0,
    "heading_number": 1.0,
    "heading_similarity": 0.96,
    "length_ratio": 0.88,
    "toc_anchor_match": 1.0
  },
  "method": "deterministic_weighted",
  "review_required": false
}
```


### Tầng 2: Block alignment có anchor

Map các block HTML trong phạm vi một cặp chapter đã xác nhận:

- Heading với heading.
- Paragraph với paragraph.
- `blockquote` với `blockquote`.
- Verse/poetry với verse/poetry.
- List item với list item.
- Table cell với table cell.
- Footnote/endnote với footnote/endnote.
- Image/caption với image/caption.

Không được flatten toàn chapter thành text trước; làm vậy sẽ mất định danh XPath, làm hỏng evidence và khiến audit không biết lỗi ở đúng chỗ nào.

Tạo anchor mạnh từ:

- Heading, số, ngày, giờ, tiền, ký hiệu.
- Tên riêng từ glossary/entity dictionary.
- URL, email, ISBN, mã số.
- Footnote ID/link (`noteref`, `fn`, `endnote`).
- HTML ID/anchor còn được giữ giữa hai bản.
- Paragraph sequence và type sequence.

Ví dụ anchor an toàn:

```text
Source: “... ngày 15 tháng 8, tại Đông Kinh ...”
Target: “... ngày 15 tháng 8, tại Tokyo ...”
```

Dù text khác ngôn ngữ, `15`, `8` và entity `Đông Kinh/Tokyo` tạo tín hiệu map mạnh.

### Tầng 3: Segment alignment bằng dynamic programming

Trong từng block/paragraph đã map, tách câu/segment rồi dùng dynamic programming để chọn đường đi có tổng cost thấp nhất.

Đừng chỉ cho phép `1:1`. Hỗ trợ:

```text
1:1   một câu ↔ một câu
1:2   một câu nguồn ↔ hai câu đích
2:1   hai câu nguồn ↔ một câu đích
2:2   hai câu nguồn ↔ hai câu đích
1:0   khả năng bỏ sót
0:1   khả năng thêm nội dung
```

Các mô hình length-based như Gale–Church tận dụng tương quan độ dài giữa các câu tương ứng và dùng dynamic programming để chọn phương án alignment có likelihood tốt nhất. Phương pháp này đặc biệt hữu ích như một lớp heuristic rẻ và nhanh, nhưng không đủ tin cậy để tự quyết các mapping khó, nhất là với dịch văn học có tách/gộp/cải biên câu.[^4_3][^4_4][^4_5]

Hàm cost đề xuất:

$$
C(i,j) =
w_l C_{\text{length}} +
w_a C_{\text{anchor}} +
w_s C_{\text{structure}} +
w_n C_{\text{number}} +
w_e C_{\text{entity}} +
w_p C_{\text{position}} +
w_m C_{\text{semantic}}
$$

Trong đó:

- $C_{\text{length}}$: chênh lệch độ dài đã chuẩn hóa theo pair language nguồn–Việt.
- $C_{\text{anchor}}$: phạt khi số, marker, tên thực thể rõ ràng không xuất hiện tương ứng.
- $C_{\text{structure}}$: phạt nếu paragraph ghép với note/table/heading bất hợp lý.
- $C_{\text{number}}$: phạt cao với ngày, số tiền, tỷ lệ, cấp bậc, tuổi không map.
- $C_{\text{entity}}$: đánh giá overlap sau khi chuẩn hóa alias bằng glossary.
- $C_{\text{position}}$: phạt mapping nhảy quá xa theo thứ tự.
- $C_{\text{semantic}}$: chỉ tính với low-confidence candidates, do embedding/AI reviewer cung cấp.

Thiết lập trọng số ban đầu:

```yaml
alignment:
  weights:
    length: 0.18
    anchors: 0.25
    structure: 0.12
    numbers: 0.18
    entities: 0.17
    position: 0.10
    semantic: 0.35
  semantic_only_when_confidence_below: 0.84
  maximum_source_sentences_per_link: 2
  maximum_target_sentences_per_link: 2
  skip_penalty_source: 4.0
  skip_penalty_target: 4.0
  review_below_confidence: 0.84
  reject_below_confidence: 0.55
```

`semantic` là một penalty/factor dùng ở vòng fallback, không chạy đại trà cùng tất cả feature. Vì vậy tổng nhóm trọng số không nhất thiết phải bằng 1.

### Tầng 4: Windowing và checkpoints

Với EPUB lớn, không chạy dynamic programming trên toàn sách hay toàn chapter dài. Dùng cửa sổ có overlap:

```text
Chapter
├── Window 01: blocks 001–050
├── Window 02: blocks 041–090
├── Window 03: blocks 081–130
└── ...
```

Quy tắc vận hành:

- Chunk theo block trước, không theo token thuần.
- Mỗi window có overlap 10–20% để tránh mất map ở biên.
- Chốt các anchor high-confidence làm “hard delimiter”.
- Chạy DP chỉ trong khoảng giữa hai hard delimiters.
- Với chapter quá dài, dùng paragraph alignment trước; chỉ sentence-align trong block có rủi ro hoặc confidence thấp.
- Lưu kết quả theo chapter/window vào SQLite ngay sau khi hoàn thành.
- `--resume` chỉ chạy các window chưa có status `completed`.
- Khi một window thay đổi do human override, chỉ invalidate các window lân cận thay vì rerun toàn sách.

Cách anchor trước, rồi align khoảng text nằm giữa các anchor bằng heuristic/length-based alignment, là một chiến lược đã được dùng để giảm độ khó của alignment.[^4_6]

### Tầng 5: Gemini chỉ review low-confidence

Đặt ngưỡng rõ ràng:


| Confidence | Xử lý |
| --: | :-- |
| ≥ 0,95 | Auto-accept, không gọi AI |
| 0,84–0,95 | Auto-accept nhưng audit semantic có context |
| 0,55–0,84 | Gemini Alignment Reviewer xác minh |
| < 0,55 | Đưa human-review queue hoặc block audit nghĩa |
| `1:0`/`0:1` | Audit completeness bắt buộc, không tự xem là alignment hợp lệ |

Prompt Gemini reviewer chỉ nhận 3–5 candidate mappings gần nhất, không hỏi câu mở “hãy map chương này”. Output phải là một trong:

```json
{
  "decision": "accept_candidate | merge_segments | split_segments | missing_source | added_target | needs_human_review",
  "selected_candidate_id": "candidate_03",
  "confidence": 0.91,
  "evidence": ["shared date 15/08", "same named entity"],
  "reason_vi": "..."
}
```


### Prompt copy-paste: Ticket alignment

```text
Bạn là senior Python/NLP engineer. Hãy triển khai Phase Alignment cho repository epub-translate-audit.

Bối cảnh:
- Tool audit EPUB source → Vietnamese target.
- EPUB phải được đọc theo OPF spine, giữ xhtml_path, XPath, block type, raw text và normalized text.
- Không sửa input EPUB.
- Alignment cần chạy được cho sách vài trăm chương, có checkpoint/resume qua SQLite.
- Không gọi Gemini cho các mapping high-confidence.

Yêu cầu:
1. Tạo package `src/epub_translate_audit/alignment/`.
2. Implement data model cho ChapterAlignment, BlockAlignment, SegmentAlignment, AlignmentCandidate và AlignmentReviewQueue.
3. Implement chapter alignment theo spine order, TOC/heading, number extraction, file name, type, length ratio.
4. Implement block alignment theo sliding window + anchors; anchor gồm heading, numbers/dates, glossary aliases, footnote marker, IDs/anchors.
5. Implement sentence/segment alignment bằng dynamic programming, cho phép 1:1, 1:2, 2:1, 2:2, 1:0, 0:1.
6. Không flatten XHTML toàn chapter; giữ link về XPath và block ID.
7. Implement confidence score, hard delimiters, overlap window, persistence SQLite, status pending/completed/review_required.
8. Đưa các mapping confidence < 0.84 vào review queue; < 0.55 không được auto-accept.
9. Viết pytest cho: 1:1, split 1:2, merge 2:1, missing source, added target, ambiguous chapters, resume run.
10. Chạy test và báo cáo các file tạo/sửa, test đã pass, giới hạn còn lại.

Không dùng LLM trong phase này. Code phải typed, có docstring ngắn, không hard-code đường dẫn.
```


## 2. Static QA ruleset tiếng Việt

Static QA không cố gắng “chấm văn hay”; nó bắt các lỗi khách quan, lỗi có pattern, và cờ rủi ro để Gemini/human đọc sâu. Phải chạy 100% trên toàn sách.

### Kiến trúc rule engine

```text
Rule
├── id: TECH-EPUB-001
├── category/subcategory
├── severity mặc định
├── scope: book | chapter | block | segment | alignment
├── preconditions
├── detector
├── evidence builder
├── confidence
├── remediation hint
└── suppress/override key
```

Interface gợi ý:

```python
class BaseRule(Protocol):
    rule_id: str
    scope: Literal["book", "chapter", "block", "segment", "alignment"]

    def evaluate(self, context: RuleContext) -> list[AuditIssue]:
        ...
```

Mỗi lỗi cần đưa ra evidence chính xác, không chỉ “chapter này có vấn đề”.

### Nhóm A: EPUB và cấu trúc

| Rule ID | Phát hiện | Severity mặc định |
| :-- | :-- | :-- |
| TECH-EPUB-001 | EPUB/ZIP/container.xml/OPF không hợp lệ | Critical |
| TECH-EPUB-002 | Spine item thiếu manifest hoặc resource không tồn tại | Critical |
| TECH-EPUB-003 | `nav.xhtml`/NCX lỗi link hoặc target anchor không tồn tại | Major |
| TECH-EPUB-004 | Chapter source có nhưng target mất | Critical |
| TECH-EPUB-005 | Target có chapter trùng/hash gần giống bất thường | Major |
| TECH-EPUB-006 | Sai reading order hoặc chapter reorder | Critical |
| TECH-EPUB-007 | Mất image, SVG, table, caption hoặc alt text có ý nghĩa | Major |
| TECH-EPUB-008 | Footnote/endnote link, backlink hoặc marker bị hỏng | Major |
| TECH-EPUB-009 | HTML tag không đóng, nesting lỗi hoặc entity encoding hỏng | Major |
| TECH-EPUB-010 | CSS/class/ID cần cho hiển thị hoặc link bị mất | Minor/Major |

### Nhóm B: Completeness và nguồn còn sót

| Rule ID | Detector gợi ý | Severity |
| :-- | :-- | :-- |
| COMP-001 | Source block không map với target block | Critical/Major |
| COMP-002 | Target block không map với source block | Major |
| COMP-003 | Đoạn target rỗng trong khi source có text meaningful | Major |
| COMP-004 | Tỷ lệ length source–target vượt ngưỡng adaptive | Flag → AI |
| COMP-005 | Câu/đoạn target lặp trong chapter hoặc giữa chapter | Major |
| COMP-006 | Chunk boundary overlap gây lặp đầu/cuối đoạn | Major |
| COMP-007 | Phát hiện source-language residue | Major |
| COMP-008 | Placeholder/token không được dịch đúng policy | Major |
| COMP-009 | Nội dung bị cắt giữa quote/tag/note | Major |

`COMP-004` phải cẩn trọng: độ dài bản dịch Việt khác source là bình thường. Rule chỉ flag outlier theo phân phối của chính cuốn sách, ví dụ robust z-score/MAD, không dùng một tỷ lệ cố định cho mọi sách.

### Nhóm C: Số, thời gian, ký hiệu và dữ kiện cứng

| Rule ID | Cách kiểm |
| :-- | :-- |
| FACT-001 | Số nguyên/thập phân/percentage map source–target |
| FACT-002 | Ngày tháng, giờ, khoảng thời gian, thứ tự |
| FACT-003 | Tiền tệ, đơn vị đo, nhiệt độ, khoảng cách, tuổi |
| FACT-004 | Tỷ lệ, cấp bậc, level, thứ hạng, phần/chương |
| FACT-005 | Phủ định, lượng từ, comparative/superlative trigger |
| FACT-006 | Mathematical expression, code, URL, email, ISBN giữ nguyên |
| FACT-007 | Quote/nested quote count bất thường |
| FACT-008 | Bracket/parenthesis/ellipsis/em-dash pair mismatch |

Với `FACT-001`, đừng yêu cầu literal equality. Cần có normalizer:

```text
one ↔ một ↔ 1
twenty-five ↔ hai mươi lăm ↔ 25
$10 ↔ 10 đô-la Mỹ
3rd ↔ thứ ba ↔ 3
```

Nếu target đổi đơn vị hợp lệ theo editorial policy, rule chỉ flag để verify chứ không auto kết luận lỗi.

### Nhóm D: Glossary, entity và xưng hô

| Rule ID | Phát hiện |
| :-- | :-- |
| TERM-001 | Term nguồn có entry glossary nhưng target khác bản chuẩn |
| TERM-002 | Forbidden variant xuất hiện |
| TERM-003 | Một source term tương ứng nhiều target variant không cho phép |
| ENT-001 | Tên nhân vật/địa danh/tổ chức/item sai hoặc drift |
| ENT-002 | Alias bị đổi hoặc lẫn 2 thực thể |
| ENT-003 | Gender/title/rank mismatch theo entity bible |
| REL-001 | Xưng hô vi phạm relationship matrix |
| REL-002 | Speaker attribution mismatch có thể detect qua cấu trúc thoại |
| REL-003 | Đại từ “hắn/cô/y/anh/chị/người đó” thiếu antecedent gần, chỉ flag |

Đừng xây xưng hô bằng regex đơn giản. Dùng `relationship matrix` theo thời gian:

```json
{
  "speaker": "char.lam",
  "listener": "char.minh",
  "chapter_range": [1, 24],
  "allowed_forms": ["cậu", "Minh", "cậu ấy"],
  "forbidden_forms": ["bệ hạ", "lão gia"],
  "register": "informal"
}
```


### Nhóm E: Vietnamese lint

Đây là static lint, cần severity thấp hơn semantic QA để không tạo “rác issue”.


| Rule ID | Ví dụ |
| :-- | :-- |
| VI-001 | Hai hoặc nhiều space liên tiếp, space trước punctuation |
| VI-002 | Dấu câu lặp sai: `,,`, `..`, `!!!` không có policy |
| VI-003 | Quote/dash/ellipsis không chuẩn hóa theo style guide |
| VI-004 | Lỗi dấu ngoặc mở–đóng không cân |
| VI-005 | Lỗi capitalisation sau dấu câu/heading theo policy |
| VI-006 | Repeated n-gram bất thường trong window |
| VI-007 | Từ đệm/literal-calque nằm trong denylist có cấu hình |
| VI-008 | Dấu thoại không nhất quán |
| VI-009 | Newline/paragraph break bất thường |
| VI-010 | Unicode normalization, combining marks, zero-width chars |
| VI-011 | Lẫn text từ ngôn ngữ nguồn trong câu Việt |
| VI-012 | Markdown/code/HTML literal bị lộ trong text reader-facing |

Danh sách denylist phải là **configurable**, không đóng cứng. Chẳng hạn “không khỏi”, “lập tức”, “ngay tức khắc” không tự thân là lỗi; chỉ flag khi mật độ vượt baseline hay lặp trong cửa sổ ngắn.

### Ví dụ `taxonomy.yaml`

```yaml
version: "1.0.0"

technical:
  epub_validity:
    severity: critical
  structural_parity:
    severity: critical
  markup_integrity:
    severity: major
  navigation:
    severity: major

completeness:
  missing_content:
    severity: critical
  duplicate_content:
    severity: major
  untranslated_residue:
    severity: major
  length_outlier:
    severity: minor
    action: ai_verify

facts:
  number_unit:
    severity: major
  chronology:
    severity: major
  symbol_integrity:
    severity: minor

terminology:
  glossary_violation:
    severity: major
  forbidden_variant:
    severity: major

entities:
  name_drift:
    severity: major
  title_rank:
    severity: major

consistency:
  address_form:
    severity: major
  speaker_attribution:
    severity: major

vietnamese:
  encoding:
    severity: major
  typography:
    severity: minor
  repetition:
    severity: minor
  calque_risk:
    severity: cosmetic
    action: ai_verify
```


### Prompt copy-paste: Ticket static rules

```text
Bạn là staff Python engineer. Hãy triển khai static QA ruleset cho repository epub-translate-audit.

Yêu cầu kiến trúc:
- Tạo `src/epub_translate_audit/rules/`.
- Mỗi rule implement BaseRule với `rule_id`, scope, evaluate(context) và trả về list[AuditIssue].
- Rule không được sửa EPUB hay source text.
- Mỗi finding phải có segment/block/chapter ID, evidence chính xác, confidence, severity, remediation hint.
- Rule config phải đọc từ `configs/taxonomy.yaml` và `project.audit.yaml`; không hard-code policy.
- Có suppression key để user chấp nhận exception có chủ đích.

Implement tối thiểu:
1. EPUB/OPF/spine/nav/anchor/footnote/link validation wrapper.
2. Structural parity source-target: missing/reordered/duplicate chapters and blocks.
3. Untranslated residue detector có language-aware heuristic, không flag tên riêng/URL/code.
4. Duplicate paragraph/chunk-overlap detector dùng normalized hash + fuzzy threshold.
5. Number/date/time/currency/unit extraction và source-target comparison; hỗ trợ Vietnamese number words cơ bản.
6. Placeholder/tag/inline markup/quote/bracket preservation.
7. Glossary match + forbidden variants.
8. Entity/alias drift theo JSON knowledge base.
9. Vietnamese typography/Unicode/space/punctuation/dialogue dash/repetition lint.
10. Length outlier theo median + MAD của chính cuốn sách; chỉ flag AI_VERIFY, không kết luận lỗi.

Viết pytest có fixtures cho từng rule, bao gồm false-positive cases. Export findings thành CSV/JSONL. Chạy test và báo cáo.
```


## 3. Release gate tự động

### Triết lý gate

Không dùng một con số tổng duy nhất. Một bản dịch có 95/100 vẫn không được release nếu:

- Mất một chương.
- Hỏng TOC/footnote.
- Có một lỗi Critical liên quan plot.
- Có đoạn nguồn còn sót.
- Có nhiều alignment chưa được giải quyết.
- Glossary nhân vật/cảnh giới lõi bị trôi.

Do đó, quyết định phải theo nguyên tắc **blocking gates trước, scoring sau**.

```text
Technical Gate
→ Alignment & Completeness Gate
→ Semantic Safety Gate
→ Consistency Gate
→ Literary Acceptance Gate
→ Human Sign-off Gate
→ Release Decision
```


### State machine

```text
DRAFT
  → INGESTED
  → TECHNICAL_FAIL | ALIGNED
  → INCOMPLETE_FAIL | STATIC_QA_COMPLETE
  → AI_AUDIT_IN_PROGRESS
  → REVIEW_REQUIRED
  → FAILED
  → CONDITIONAL_PASS
  → PASSED
  → RELEASED
```

`RELEASED` không được tự động set chỉ vì audit pass; cần human sign-off/explicit release command nếu policy yêu cầu.

### Gate policy mẫu

```yaml
release_policy:
  version: "1.0.0"

  hard_blocks:
    epub_validation_errors_max: 0
    missing_chapters_max: 0
    missing_meaningful_blocks_max: 0
    unresolved_alignment_max: 0
    untranslated_residue_major_max: 0
    critical_issues_max: 0
    unresolved_major_plot_issues_max: 0
    broken_navigation_links_max: 0
    broken_footnote_links_max: 0

  quality_thresholds:
    major_issues_per_1000_target_words_max: 0.30
    weighted_error_rate_per_1000_words_max: 2.00
    glossary_compliance_min: 0.985
    core_entity_compliance_min: 1.0
    core_address_compliance_min: 1.0
    source_target_coverage_min: 0.995
    accepted_alignment_confidence_min: 0.84

  audit_coverage:
    deterministic_rules_min: 1.0
    high_risk_semantic_min: 1.0
    semantic_baseline_min: 0.35
    dialogue_literary_min: 1.0
    random_post_fix_verification_min: 0.03

  human_review:
    required: true
    require_all_critical_and_major_reviewed: true
    require_first_last_chapter_review: true
    require_high_risk_chapter_review: true

  decisions:
    pass:
      all_hard_blocks_clear: true
      all_quality_thresholds_met: true
      all_required_human_signoffs_complete: true
    conditional_pass:
      all_hard_blocks_clear: true
      allowed_minor_open_issues: 20
      allowed_cosmetic_open_issues: 200
      all_required_human_signoffs_complete: true
    fail:
      otherwise: true
```


### Công thức score

Dùng score để theo dõi xu hướng, **không** dùng làm override gate.

$$
WER_{1000} =
\frac{25N_c + 5N_m + N_{mi} + 0.25N_{co}}{W_t}
\times 1000
$$

Trong đó:

- $N_c$: Critical.
- $N_m$: Major.
- $N_{mi}$: Minor.
- $N_{co}$: Cosmetic.
- $W_t$: số từ đích.

Cần có thêm hai chỉ số riêng:

$$
\text{Glossary compliance} =
\frac{\text{occurrences hợp lệ}}{\text{occurrences cần kiểm}}
$$

$$
\text{Source-target coverage} =
\frac{\text{source meaningful blocks đã map hoặc đã giải trình}}{\text{total source meaningful blocks}}
$$

### Pseudocode release engine

```python
def decide_release(metrics: AuditMetrics, policy: ReleasePolicy) -> ReleaseDecision:
    blockers: list[Blocker] = []

    check_max(blockers, "EPUB validation errors",
              metrics.epub_validation_errors,
              policy.hard_blocks.epub_validation_errors_max)

    check_max(blockers, "Missing chapters",
              metrics.missing_chapters,
              policy.hard_blocks.missing_chapters_max)

    check_max(blockers, "Unresolved alignment",
              metrics.unresolved_alignment,
              policy.hard_blocks.unresolved_alignment_max)

    check_max(blockers, "Critical issues",
              metrics.critical_open,
              policy.hard_blocks.critical_issues_max)

    check_min(blockers, "Glossary compliance",
              metrics.glossary_compliance,
              policy.quality_thresholds.glossary_compliance_min)

    if blockers:
        return ReleaseDecision(status="FAIL", blockers=blockers)

    if not metrics.required_human_signoffs_complete:
        return ReleaseDecision(
            status="REVIEW_REQUIRED",
            blockers=[Blocker("Human sign-off incomplete")]
        )

    if metrics.major_per_1000 > policy.quality_thresholds.major_issues_per_1000_target_words_max:
        return ReleaseDecision(status="FAIL", blockers=[...])

    if metrics.open_minor <= policy.decisions.conditional_pass.allowed_minor_open_issues:
        return ReleaseDecision(status="CONDITIONAL_PASS", blockers=[])

    return ReleaseDecision(status="PASS", blockers=[])
```


### Prompt copy-paste: Ticket release gates

```text
Bạn là senior backend/quality-systems engineer. Hãy triển khai release gate engine cho repository epub-translate-audit.

Mục tiêu:
- Không dùng score tổng để override lỗi Critical hoặc lỗi cấu trúc.
- Quyết định phải giải thích được bằng machine-readable blockers.
- Không tự chuyển sang RELEASED; chỉ PASS/CONDITIONAL_PASS/FAIL/REVIEW_REQUIRED.

Yêu cầu:
1. Tạo Pydantic models cho ReleasePolicy, AuditMetrics, Blocker, ReleaseDecision.
2. Đọc policy từ `configs/release_policy.yaml`.
3. Implement state machine: DRAFT, INGESTED, ALIGNED, STATIC_QA_COMPLETE, AI_AUDIT_IN_PROGRESS, REVIEW_REQUIRED, FAIL, CONDITIONAL_PASS, PASS, RELEASED.
4. Implement hard blocks: EPUB validity, missing chapter/block, unresolved alignment, untranslated residue, critical issues, unresolved plot-major issues, broken nav/note links.
5. Implement thresholds: major/1000 words, weighted error rate, glossary/entity/address compliance, source-target coverage, audit coverage.
6. Mọi decision phải có timestamp, policy version, run ID, metrics snapshot, blockers and warnings.
7. Implement JSON output `release_decision.json` và HTML summary section.
8. Write thorough pytest with boundary cases, one critical issue, missing chapter, insufficient audit coverage, incomplete human signoff, conditional pass, pass.
9. Không sửa input EPUB. Không hard-code threshold trong code.

Chạy tests và báo cáo file thay đổi.
```


## 4. Pydantic schema cho Gemini

Gemini hỗ trợ structured output theo JSON Schema; dùng Pydantic schema với `response_mime_type="application/json"` và `response_schema=<PydanticModel>` để ép output có cấu trúc, thay vì parse Markdown hoặc regex JSON thủ công. Google hiện khuyến nghị Google GenAI SDK cho Python; vì vậy repo nên dùng package `google-genai`, không dùng SDK cũ.[^4_7][^4_8][^4_9][^4_10]

### Quy tắc schema

- Schema nhỏ, cụ thể, có enum.
- Không để model tự sinh `issue_id`; app tạo ID sau khi validate.
- Cấm `extra` fields.
- Evidence bắt buộc với mọi issue.
- `source_evidence` được phép `null` chỉ cho lỗi purely target-side, ví dụ typography.
- Không dùng schema “một model cho mọi thứ” quá khổng lồ; dùng model riêng cho từng agent.
- Tách **raw AI finding** khỏi **normalized final issue** sau adjudication.
- Validate lần hai bằng business rule: quote evidence có thực sự tồn tại trong segment không.


### `schemas.py` đề xuất

```python
from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Severity(StrEnum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    COSMETIC = "cosmetic"


class AuditCategory(StrEnum):
    ACCURACY = "accuracy"
    TERMINOLOGY = "terminology"
    ENTITY = "entity"
    CONSISTENCY = "consistency"
    FLUENCY = "fluency"
    STYLE = "style"
    LOCALIZATION = "localization"
    TECHNICAL = "technical"


class Evidence(StrictModel):
    source_quote: str | None = Field(
        default=None,
        description="Exact shortest quote from source. Null only for target-only issues."
    )
    target_quote: str = Field(
        min_length=1,
        description="Exact shortest quote from Vietnamese target."
    )
    source_context_id: str | None = None
    target_context_id: str

    @field_validator("source_quote", "target_quote")
    @classmethod
    def no_generic_evidence(cls, value: str | None) -> str | None:
        if value and value.strip().lower() in {"n/a", "none", "không có", "unknown"}:
            raise ValueError("Evidence must be an exact quote, not a placeholder.")
        return value


class AIFinding(StrictModel):
    category: AuditCategory
    subcategory: str = Field(min_length=2, max_length=80)
    severity: Severity
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    evidence: Evidence
    explanation_vi: str = Field(min_length=12, max_length=1200)
    impact_vi: str = Field(min_length=8, max_length=700)
    suggested_correction_vi: str | None = Field(default=None, max_length=1200)
    requires_human_review: bool = False


class SemanticAuditResponse(StrictModel):
    agent_name: Literal["semantic_auditor"]
    segment_id: str = Field(min_length=1)
    issues: list[AIFinding] = Field(default_factory=list, max_length=12)
    no_issue_reason_vi: str | None = Field(
        default=None,
        description="Required only when issues is empty."
    )

    @field_validator("no_issue_reason_vi")
    @classmethod
    def validate_empty_result_reason(cls, value: str | None, info):
        issues = info.data.get("issues", [])
        if not issues and not value:
            raise ValueError("Explain why no material issue was found.")
        return value


class AlignmentDecision(StrEnum):
    ACCEPT_CANDIDATE = "accept_candidate"
    MERGE_SEGMENTS = "merge_segments"
    SPLIT_SEGMENTS = "split_segments"
    MISSING_SOURCE = "missing_source"
    ADDED_TARGET = "added_target"
    NEEDS_HUMAN_REVIEW = "needs_human_review"


class AlignmentReviewResponse(StrictModel):
    agent_name: Literal["alignment_reviewer"]
    decision: AlignmentDecision
    selected_candidate_id: str | None = None
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    evidence: list[str] = Field(min_length=1, max_length=6)
    reason_vi: str = Field(min_length=15, max_length=800)
```


### Gemini client với Pydantic

```python
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel
from tenacity import retry, retry_if_exception_type, stop_after_attempt
from tenacity import wait_exponential_jitter

T = TypeVar("T", bound=BaseModel)


class GeminiStructuredClient:
    def __init__(
        self,
        api_key: str,
        model: str,
        cache_dir: Path,
        temperature: float = 0.1,
    ) -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model
        self._cache_dir = cache_dir
        self._temperature = temperature
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_key(self, prompt: str, schema: type[BaseModel]) -> str:
        material = f"{self._model}|{schema.__name__}|{prompt}".encode("utf-8")
        return hashlib.sha256(material).hexdigest()

    @retry(
        retry=retry_if_exception_type((TimeoutError, ConnectionError)),
        wait=wait_exponential_jitter(initial=1, max=25),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def generate(self, prompt: str, schema: type[T]) -> T:
        cache_file = self._cache_dir / f"{self._cache_key(prompt, schema)}.json"

        if cache_file.exists():
            return schema.model_validate_json(cache_file.read_text(encoding="utf-8"))

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=self._temperature,
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )

        result = schema.model_validate_json(response.text)
        cache_file.write_text(result.model_dump_json(indent=2), encoding="utf-8")
        return result
```


### Evidence verification bắt buộc

Structured output chỉ đảm bảo **shape**; không đảm bảo Gemini trích dẫn đúng. Thêm một verifier sau Pydantic:

```python
def verify_finding_evidence(
    finding: AIFinding,
    source_text: str,
    target_text: str,
) -> list[str]:
    errors: list[str] = []

    if finding.evidence.source_quote:
        if finding.evidence.source_quote not in source_text:
            errors.append("source_quote_not_found")

    if finding.evidence.target_quote not in target_text:
        errors.append("target_quote_not_found")

    if finding.category != AuditCategory.TECHNICAL and not finding.evidence.source_quote:
        errors.append("source_evidence_required")

    return errors
```

Nếu verify lỗi:

1. Không đưa finding vào final ledger.
2. Lưu raw response vào `rejected_ai_findings.jsonl`.
3. Retry một lần với prompt yêu cầu quote chính xác.
4. Nếu vẫn sai, đưa segment vào queue hoặc bỏ finding—không được bịa evidence.

### Prompt copy-paste: Ticket Gemini schema

```text
Bạn là senior Python platform engineer. Hãy triển khai Gemini structured-output layer cho repository epub-translate-audit.

Yêu cầu:
1. Dùng official package `google-genai`, Pydantic v2 và Gemini model qua config.
2. Tạo `ai/schemas.py`, `ai/gemini_client.py`, `ai/prompt_loader.py`, `ai/evidence_verifier.py`, `ai/cache.py`.
3. Strict Pydantic models phải `extra="forbid"`.
4. Tạo schema riêng cho: BookProfileResponse, AuditPlanResponse, SemanticAuditResponse, ConsistencyAuditResponse, LiteraryAuditResponse, AlignmentReviewResponse, AdjudicationResponse.
5. Không để model tự tạo final issue_id; ứng dụng tạo sau validation.
6. Cấu hình Gemini bằng response_mime_type application/json và response_schema=PydanticModel.
7. Implement cache key gồm model ID, prompt template version/hash, rendered prompt, schema version và relevant config hash.
8. Implement timeout, bounded retries, exponential jitter, rate limiting và response validation.
9. Implement evidence verifier: source_quote/target_quote phải tồn tại trong đúng context; finding fail evidence không được vào final ledger.
10. Raw response, validation failure và retry metadata phải được log an toàn; không log API key.
11. Viết test mock Gemini client cho valid JSON, malformed JSON, schema violation, missing quote, cache hit, retry and rate limit.
12. Cập nhật README với biến GEMINI_API_KEY và nguyên tắc dữ liệu sách được gửi đến API.

Chạy tests, lint và báo cáo chi tiết.
```


## 5. Cách giao việc trong Chatbox

Dùng chiến lược: **một prompt = một pull-request-sized change**. Mỗi lần chỉ yêu cầu AI thực hiện tối đa một module hoặc một phase có liên quan chặt.

### Prompt mở đầu thiết lập luật dự án

Paste một lần khi mở Chatbox trong root repository:

```text
Bạn đang là principal engineer của project `epub-translate-audit`.

Quy tắc bắt buộc:
- Đọc README.md, pyproject.toml, configs/ và code liên quan trước khi sửa.
- Không tự đổi public data contract, CLI option, config key hoặc taxonomy nếu chưa giải thích migration.
- Input EPUB là immutable; tuyệt đối không sửa file input.
- Mọi output phải trace được về run_id, source/target hash, config version, prompt version và model.
- Mọi AI output phải được Pydantic validate và evidence-verify trước khi vào final issue ledger.
- Không hard-code API key, đường dẫn máy, model, threshold, glossary hay source language.
- Viết/điều chỉnh pytest cho hành vi mới; chạy test và lint trước khi kết luận.
- Khi chưa rõ, đọc code và nêu assumption trước; không tự ý thay đổi kiến trúc lớn.
- Khi hoàn tất, trả về: mục tiêu hoàn thành, file thay đổi, lệnh test đã chạy, kết quả test, giới hạn/rủi ro còn lại.
- Không commit, push, cài global package hoặc xóa file nếu tôi chưa yêu cầu.
```


### Chuỗi triển khai khuyến nghị

| Thứ tự | Ticket cho Chatbox | Definition of done |
| --: | :-- | :-- |
| 1 | Bootstrap repo, CLI, config, logging, run manifest | `epub-audit --help` chạy được |
| 2 | EPUB ingestion và EPUBCheck wrapper | Đọc spine/OPF/nav, xuất manifest |
| 3 | Block extractor và segmenter | Xuất segment ổn định, giữ XPath |
| 4 | Alignment deterministic | Map chapter/block/segment, review queue |
| 5 | Static rules | Xuất findings cho toàn corpus |
| 6 | Gemini structured layer | Cache, schema, retries, evidence verify |
| 7 | Book profiler và adaptive planner | Sinh `audit_plan.json` |
| 8 | Semantic/consistency/literary agents | Sinh raw findings hợp schema |
| 9 | Adjudication và CAPA | Final issue ledger, clusters, root cause |
| 10 | Release gate | `release_decision.json` đúng policy |
| 11 | Report HTML/XLSX/Power BI export | Artifact dùng được cho review/dashboard |
| 12 | E2E fixture, regression suite, docs/CI | Có thể chạy lại ổn định |

### Prompt review sau mỗi ticket

```text
Hãy review phần bạn vừa triển khai như một code reviewer độc lập.

Kiểm tra:
1. Có vi phạm input EPUB immutable không?
2. Có path/model/threshold/API key hard-code không?
3. Có hành vi không idempotent hoặc không resume-safe không?
4. AI output có thể lọt qua khi không valid schema/evidence không?
5. Có false positive nguy hiểm trong alignment/rules không?
6. Test có cover failure modes và boundary cases không?
7. Có thay đổi contract mà README/config/test chưa cập nhật không?

Sửa các lỗi phát hiện được, chạy lại test/lint, rồi báo cáo diff logic và rủi ro còn lại.
```


## Thứ tự triển khai thực tế

Anh/chị nên bắt đầu ngay bằng ba ticket theo thứ tự sau:

1. **EPUB ingestion + manifest**: nếu không xác định đúng spine/XHTML/nav thì mọi module sau đều sai nền.
2. **Segmenter + deterministic alignment**: đây là điểm quyết định chất lượng audit và chi phí Gemini.
3. **Static QA ruleset + release engine cơ bản**: tạo giá trị ngay cả khi Gemini chưa tích hợp.

Chỉ sau khi ba phần trên có test và output ổn định mới tích hợp Gemini structured output. Làm như vậy giúp giảm đáng kể token/API calls: Gemini chỉ xem segment khó, rủi ro cao hoặc cần đánh giá ngữ nghĩa–văn phong; hệ thống không tốn AI cho những lỗi có thể xác minh bằng cấu trúc EPUB, hash, regex, glossary và thuật toán alignment.

<span style="display:none">[^4_11][^4_12][^4_13][^4_14][^4_15][^4_16][^4_17][^4_19][^4_20][^4_21]</span>

<div align="center">⁂</div>

[^4_1]: https://www.w3.org/TR/epub-overview-33/

[^4_2]: https://help.apple.com/itc/booksassetguide/en.lproj/itccdf8e5ab3.html

[^4_3]: https://aclanthology.org/W12-4212.pdf

[^4_4]: https://www.site.uottawa.ca/~nat/Courses/NLP-Course/Old-Version/NLP-Lecture-13/tsld008.htm

[^4_5]: https://mt-archive.net/90/IBM-1993-Simard.pdf

[^4_6]: https://aclanthology.org/2010.amta-papers.14.pdf

[^4_7]: https://ai.google.dev/gemini-api/docs/structured-output

[^4_8]: https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-structured-outputs/

[^4_9]: https://ai.google.dev/gemini-api/docs/libraries

[^4_10]: https://github.com/googleapis/python-genai

[^4_11]: image.jpg

[^4_12]: https://snapintel.io/blog/mqm-vs-lisa-qa-model-which-translation-quality-framework-should-you-use

[^4_13]: https://ai.google.dev/gemini-api/docs/generate-content/structured-output

[^4_14]: https://dl.acm.org/doi/10.3115/981574.981576

[^4_15]: https://www.w3.org/TR/epub-33/

[^4_16]: https://www.ida.liu.se/~jodfo01/gslt/bitext-alignment-jody.pdf

[^4_17]: https://en.wikipedia.org/wiki/Gale–Church_alignment_algorithm

[^4_18]: https://github.com/alvations/gachalign

[^4_19]: https://github.com/loomchild/maligna

[^4_20]: https://citeseerx.ist.psu.edu/document?repid=rep1\&type=pdf\&doi=917f88692f329a927b2e42ca232905eebdf77feb

[^4_21]: https://s3.amazonaws.com/tm-town-nlp-resources/sent-align.pdf


---

# tôi muốn AI là bên audit thủ công chứ không chạy bằng scripts để audit nội dung, nhưng các model flash làm việc rất sơ sài

Đúng, nếu dùng Flash như một “reviewer thủ công” mà chỉ đưa yêu cầu kiểu *“hãy audit bản dịch này”*, nó thường trả lời rất hời hợt: vài nhận xét chung, bỏ sót lỗi nghĩa tinh tế, hoặc soi những lỗi văn phong vụn vặt thay vì lỗi cốt truyện. Vấn đề thường không nằm ở việc Flash hoàn toàn không audit được, mà ở **thiết kế phiên audit**: phạm vi quá rộng, thiếu bằng chứng bắt buộc, thiếu ngữ cảnh và không có cơ chế buộc model tự kiểm tra từng hạng mục.

Với mục tiêu của anh/chị, nên chuyển kiến trúc từ “script audit nội dung” sang **AI-led manual audit**: script chỉ làm công tác thư ký—tách EPUB, gửi từng packet, lưu trạng thái, gom kết quả—còn AI thực hiện công việc đọc, suy luận, đối chiếu và kết luận như một biên tập viên/auditor. Gemini Flash có thể làm tốt vai trò này nếu được chia nhỏ nhiệm vụ, cấp context đúng và áp rubric có bằng chứng bắt buộc. Google cũng khuyến nghị dùng cấu trúc prompt nhất quán, delimiters rõ ràng, đặt yêu cầu quan trọng ở đầu, và để instruction cụ thể ở cuối sau khi đã cung cấp long context.[^5_1][^5_2]

## Đổi mô hình vận hành

### Không dùng scripts để “chấm nội dung”

Script không được tự kết luận:

- “Câu này dịch sai.”
- “Văn chưa tự nhiên.”
- “Xưng hô sai.”
- “Lỗi văn phong.”
- “Tình tiết mâu thuẫn.”

Script chỉ được làm các việc cơ học:

1. Đọc EPUB theo spine và tách ra thành Part → Chapter → Scene/Block → Audit Packet.
2. Đưa source, target, context, glossary và knowledge base đúng phần vào prompt.
3. Chọn packet nào cần AI đọc sâu, theo kế hoạch do **AI planner** lập.
4. Lưu câu trả lời, giữ checkpoint, chống gửi trùng và tạo review queue.
5. Chuẩn hóa output thành bảng để anh/chị review/sửa.
6. Cảnh báo kỹ thuật như thiếu chapter, bị lặp chunk, HTML hỏng—đây không phải đánh giá nội dung.

Nói cách khác:

```text
Script = trợ lý vận hành / hồ sơ kiểm toán
Gemini Flash = auditor đọc song ngữ
Model mạnh hơn hoặc human = chief editor / người phân xử
Anh/chị = người quyết định editorial policy và release
```


## Vì sao Flash audit sơ sài

### 1. Nhiệm vụ quá bao quát

Nếu yêu cầu Flash cùng lúc kiểm “đúng nghĩa, văn hay, xưng hô, thuật ngữ, logic, văn hóa, footnote, EPUB”, nó sẽ chọn một vài lỗi dễ thấy rồi kết thúc. Đây là giới hạn phân bổ attention, không hẳn là do nó không biết kiểm.

Cách sửa: **một lượt audit chỉ có một objective chính**.


| Lượt | Flash chỉ làm gì | Không làm gì |
| :-- | :-- | :-- |
| Semantic pass | Đối chiếu nghĩa source–target | Không polish văn |
| Continuity pass | Nhân vật, xưng hô, thực thể, timeline | Không soi từng dấu phẩy |
| Literary pass | Độ tự nhiên, voice, nhịp, subtext | Không kết luận sai nghĩa nếu không chắc |
| Localization pass | Điển cố, tên riêng, chú thích, register | Không rewrite cả đoạn |
| Scene pass | Mạch cảnh, motive, causal chain | Không audit từng câu đơn lẻ |
| Final red-team | Tìm lỗi bị bỏ sót | Không lập lại lỗi đã ghi nhận |

Gemini khuyến nghị chia các bài toán nhiều bước thành các nhiệm vụ tập trung hơn thay vì ép một call xử lý logic phức tạp.[^5_3][^5_4]

### 2. Không bị buộc phải “chứng minh đã đọc”

Flash rất dễ trả ra: *“Bản dịch nhìn chung ổn, có vài câu chưa tự nhiên.”* Điều này vô dụng.

Mỗi finding phải bắt buộc có:

- Trích dẫn nguyên văn nguồn.
- Trích dẫn nguyên văn đích.
- Loại lỗi.
- Vì sao hai đoạn không tương ứng hoặc vì sao tiếng Việt không đạt.
- Mức ảnh hưởng.
- Gợi ý sửa tối thiểu.
- Mức độ chắc chắn.
- Đánh dấu có cần human review không.

Nếu không có evidence, finding không được chấp nhận. Nếu không có lỗi, model phải nêu rõ **những kiểm tra nào đã hoàn thành** chứ không chỉ ghi “không phát hiện”.

### 3. Context bị nghèo

Một đoạn tiểu thuyết 300 chữ không thể audit chuẩn nếu không biết:

- Ai đang nói và nói với ai.
- Quan hệ hiện tại.
- Tên gọi/xưng hô được chấp thuận.
- Thuật ngữ, cảnh giới, chức vị.
- Trước đó xảy ra gì.
- Cảnh đang thuộc thể loại/nhịp nào.
- Quy ước dịch và mức cổ phong được mong muốn.

Anh/chị vốn đã có knowledge folder về quan hệ, giọng, tone và xưng hô. Đây chính là tài sản quan trọng để tăng chất lượng audit: mỗi packet chỉ nên nạp **knowledge liên quan**, thay vì nhét cả bible vào mọi call.

### 4. Không có “điểm dừng” rõ ràng

Flash hay ngừng sớm vì prompt không quy định định nghĩa hoàn thành. Hãy bắt nó đi qua checklist và báo cáo coverage.

Ví dụ:

```text
Không được kết thúc audit trước khi lần lượt kiểm:
[ ] Chủ thể, hành động, đối tượng
[ ] Phủ định, mức độ, thời–thể, nguyên nhân–kết quả
[ ] Tên riêng, số, chức vị, thuật ngữ
[ ] Đại từ và người nói
[ ] Bỏ sót/thêm diễn giải
[ ] Register, xưng hô và sắc thái
[ ] Tính tự nhiên của tiếng Việt
```

Và yêu cầu model trả:

```json
{
  "completed_checks": [
    "agency_and_action",
    "negation_modality",
    "entity_terminology",
    "reference_and_speaker",
    "omission_addition",
    "vietnamese_fluency"
  ],
  "issues": []
}
```

Không nên đánh đồng “Flash không tìm lỗi” với “đoạn đạt”. Nó chỉ là: *Flash không tìm thấy lỗi trong các hạng mục nó xác nhận đã đọc*.

## Cấu trúc audit thủ công bằng AI

### Audit packet lý tưởng

Đừng gửi từng câu tách rời. Đơn vị audit tốt nhất cho sách thường là **scene packet** hoặc **micro-chapter packet**, khoảng 800–2.500 từ mỗi ngôn ngữ, tùy mật độ thoại và độ phức tạp.

```text
<AUDIT_BRIEF>
Book: ...
Target language: Vietnamese
Genre and register: ...
Audit pass: semantic_accuracy
Strictness: publication-grade
</AUDIT_BRIEF>

<EDITORIAL_POLICY>
- Tên riêng: ...
- Xưng hô: ...
- Thuật ngữ: ...
- Quy tắc chú thích: ...
- Mức độ Việt hóa: ...
</EDITORIAL_POLICY>

<RELEVANT_KNOWLEDGE>
- Character A: ...
- Character B: ...
- Relationship and allowed forms: ...
- Terms appearing in this scene: ...
- Prior plot facts required to interpret this scene: ...
</RELEVANT_KNOWLEDGE>

<PREVIOUS_CONTEXT>
[150–400 từ nguồn + đích của phần trước]
</PREVIOUS_CONTEXT>

<FOCUS_SOURCE>
[800–2.500 từ source]
</FOCUS_SOURCE>

<FOCUS_TARGET>
[800–2.500 từ Vietnamese translation]
</FOCUS_TARGET>

<NEXT_CONTEXT>
[100–250 từ nguồn + đích phía sau]
</NEXT_CONTEXT>

<TASK>
...
</TASK>
```

Cấu trúc có delimiter rõ như vậy giảm khả năng model lẫn source, target và instructions. Google khuyến nghị cấu trúc nhất quán bằng XML-style tags hoặc Markdown headings, đồng thời đặt long context trước rồi đưa yêu cầu cụ thể ở cuối.[^5_2][^5_1]

### Kích thước packet

| Loại cảnh | Kích thước focus đề xuất | Context trước/sau |
| :-- | --: | --: |
| Độc thoại, miêu tả đơn giản | 1.500–2.500 từ mỗi ngôn ngữ | 150–250 từ |
| Thoại 2–3 nhân vật | 800–1.500 từ mỗi ngôn ngữ | 250–400 từ |
| Điều tra, suy luận, twist | 600–1.000 từ mỗi ngôn ngữ | 400–700 từ |
| Cổ phong, điển cố, thơ/câu đối | 300–800 từ mỗi ngôn ngữ | 300–500 từ |
| Combat/hệ thống/cảnh giới | 700–1.200 từ mỗi ngôn ngữ | 300–500 từ |

Một packet quá lớn sẽ khiến Flash bỏ qua chi tiết. Packet quá nhỏ thì mất logic. Với source–target song ngữ, hãy ưu tiên một “cảnh nhỏ hoàn chỉnh” hơn là cố định đúng số token.

## Prompt audit sâu cho Flash

Dưới đây là prompt thực dụng để thay thế yêu cầu audit chung chung. Có thể dùng làm `semantic_auditor.md`.

```text
<SYSTEM_ROLE>
Bạn là một biên tập viên dịch thuật song ngữ cấp xuất bản, chuyên audit tiểu thuyết và sách dài.
Bạn đang làm QA thủ công với tiêu chuẩn phát hành thương mại, không phải đưa nhận xét chung chung.

Bạn phải đọc đầy đủ SOURCE và TARGET trong phạm vi FOCUS, dùng CONTEXT chỉ để giải quyết tham chiếu, người nói, quan hệ, động cơ và diễn biến.

Không tự dịch lại toàn bộ đoạn.
Không khen chung chung.
Không nêu lỗi nếu không trích được bằng chứng nguyên văn.
Không coi khác biệt câu chữ là lỗi nếu nghĩa, sắc thái và chức năng văn chương vẫn được giữ.
</SYSTEM_ROLE>

<AUDIT_OBJECTIVE>
Pass hiện tại: SEMANTIC_ACCURACY.

Mục tiêu duy nhất:
Phát hiện mọi lỗi đáng kể làm bản dịch tiếng Việt sai hoặc suy giảm nghĩa của nguyên tác.

Phải kiểm lần lượt:
1. Chủ thể, hành động, đối tượng, quan hệ sở hữu.
2. Phủ định, tình thái, mức độ, thời điểm, thứ tự và nguyên nhân–kết quả.
3. Bỏ sót, thêm ý, tự diễn giải, lặp hoặc chưa dịch.
4. Danh từ riêng, số, thời gian, cấp bậc, chức vị, thuật ngữ.
5. Đại từ, người nói, người được nhắc tới và quan hệ giữa nhân vật.
6. Hàm ý, mỉa mai, lời đe dọa, cảm xúc và thông tin được cố ý mơ hồ.
7. Thông tin có thể ảnh hưởng logic cảnh này hoặc cốt truyện về sau.

Không audit ngữ pháp, dấu câu hay độ văn hoa, trừ khi chúng làm đổi nghĩa.
</AUDIT_OBJECTIVE>

<SEVERITY_POLICY>
CRITICAL: Đảo/làm mất thông tin then chốt, hỏng logic cốt truyện, sai người–sự kiện–quan hệ trọng yếu.
MAJOR: Sai nghĩa rõ ràng, bỏ/thêm ý quan trọng, sai thuật ngữ hay xưng hô lõi, thay đổi động cơ hoặc sắc thái lớn.
MINOR: Lệch nghĩa nhỏ nhưng vẫn hiểu mạch chính.
COSMETIC: Không dùng trong pass này.
</SEVERITY_POLICY>

<EDITORIAL_POLICY>
{{EDITORIAL_POLICY}}
</EDITORIAL_POLICY>

<RELEVANT_KNOWLEDGE>
{{RELEVANT_KNOWLEDGE}}
</RELEVANT_KNOWLEDGE>

<PREVIOUS_CONTEXT>
{{PREVIOUS_SOURCE_AND_TARGET}}
</PREVIOUS_CONTEXT>

<FOCUS_SOURCE>
{{FOCUS_SOURCE}}
</FOCUS_SOURCE>

<FOCUS_TARGET>
{{FOCUS_TARGET}}
</FOCUS_TARGET>

<NEXT_CONTEXT>
{{NEXT_SOURCE_AND_TARGET}}
</NEXT_CONTEXT>

<MANDATORY_WORKFLOW>
Trước khi kết luận, phải hoàn thành đủ checklist:
- agency_action_object
- negation_modality_degree
- temporal_causal_logic
- omission_addition_untranslated
- named_entity_term_number
- pronoun_speaker_reference
- implication_tone_ambiguity
- plot_relevance

Với mỗi lỗi, nêu quote NGẮN NHẤT nhưng đủ chứng minh từ SOURCE và TARGET.
Nếu không có lỗi material, vẫn phải báo completed_checks và nêu 2–5 điểm khó đã đối chiếu.
</MANDATORY_WORKFLOW>

<OUTPUT_CONTRACT>
Chỉ trả về JSON hợp lệ theo schema sau. Không markdown. Không prose ở ngoài JSON.

{
  "audit_pass": "semantic_accuracy",
  "packet_id": "{{PACKET_ID}}",
  "coverage": {
    "source_focus_read": true,
    "target_focus_read": true,
    "completed_checks": [
      "agency_action_object",
      "negation_modality_degree",
      "temporal_causal_logic",
      "omission_addition_untranslated",
      "named_entity_term_number",
      "pronoun_speaker_reference",
      "implication_tone_ambiguity",
      "plot_relevance"
    ],
    "difficult_points_checked": [
      {
        "source_quote": "...",
        "target_quote": "...",
        "verification_note_vi": "..."
      }
    ]
  },
  "issues": [
    {
      "category": "accuracy",
      "subcategory": "mistranslation|omission|addition|untranslated|reference|negation|modality|number_or_unit|chronology_or_causality|implication",
      "severity": "critical|major|minor",
      "confidence": 0.00,
      "source_quote": "...",
      "target_quote": "...",
      "explanation_vi": "...",
      "impact_vi": "...",
      "suggested_correction_vi": "...",
      "needs_human_review": true
    }
  ],
  "no_material_issue_reason_vi": "Điền khi issues rỗng; không dùng câu chung chung."
}
</OUTPUT_CONTRACT>
```


## Chạy audit nhiều pass

Đừng dùng một prompt cố “audit toàn diện”. Chạy tuần tự để Flash có một nhiệm vụ tập trung trong từng pass.


| Pass | Đơn vị audit | Câu hỏi bắt buộc |
| :-- | :-- | :-- |
| 0. Book profiling | 3–5 mẫu đại diện + metadata | Đây là sách gì, rủi ro gì, cần chuẩn audit nào? |
| 1. Semantic accuracy | Scene packet song ngữ | Có sai/bỏ/thêm/lệch nghĩa không? |
| 2. Entity \& continuity | Theo chapter/arc | Tên, quan hệ, xưng hô, timeline có trôi không? |
| 3. Dialogue audit | Các scene thoại | Ai nói, nói với ai, register và hàm ý có đúng không? |
| 4. Literary Vietnamese | Chỉ target + source tham chiếu | Có đọc tự nhiên, đúng voice/thể loại không? |
| 5. Red-team | Những packet đã Pass | Nếu phải tìm 1–3 lỗi bị bỏ sót, chúng ở đâu? |
| 6. Fix verification | Chỉ các issue đã sửa | Sửa có đúng nguyên tác, tạo lỗi mới hay không? |

Pass 5 đặc biệt quan trọng với Flash. Lượt đầu thường có xu hướng “đạt yêu cầu”; red-team prompt buộc nó mặc định hoài nghi và chỉ tìm những lỗi material bị audit trước bỏ qua.

### Prompt red-team

```text
Bạn là red-team reviewer độc lập. Một auditor trước đó đã kết luận packet này không có lỗi material hoặc đã liệt kê các lỗi bên dưới.

Không lặp lại lỗi cũ trừ khi severity của chúng bị đánh giá thấp.
Nhiệm vụ của bạn là tìm tối đa 3 lỗi material mà auditor trước có khả năng bỏ sót.

Ưu tiên:
1. Đảo chủ thể/đối tượng hoặc đại từ.
2. Phủ định, điều kiện, mức độ, thời gian, nguyên nhân–kết quả.
3. Bỏ sót thông tin mấu chốt nhưng ít nổi bật.
4. Hàm ý, mỉa mai, lời nói nước đôi.
5. Sai xưng hô hoặc sai quan hệ làm lệch tính cách/cảnh.

Nếu không tìm được lỗi mới, phải nêu chính xác ba điểm khó đã được kiểm đối chiếu và vì sao chúng vẫn đúng.

SOURCE:
{{SOURCE}}

TARGET:
{{TARGET}}

KNOWN_ISSUES:
{{KNOWN_ISSUES}}

Chỉ trả JSON theo schema AuditResponse. Mỗi finding bắt buộc có quote source và target.
```


## Tăng “độ chăm” của Flash

### Dùng thinking budget nếu model hỗ trợ

Nếu đang dùng Gemini 2.5 Flash và API/UI cho phép, đừng để thinking ở mức thấp hoặc bị disable. Gemini 2.5 Flash hỗ trợ `thinkingBudget` từ 0 đến 24.576 token; giá trị cao hơn cho phép model suy luận lâu hơn, dù chi phí và latency tăng. Dynamic thinking có thể được bật bằng giá trị `-1`; tài liệu cũng nêu Flash có thể điều chỉnh budget theo độ phức tạp của prompt.[^5_5][^5_6][^5_7]

Khuyến nghị thực tế:


| Pass | Thinking budget gợi ý | Temperature |
| :-- | --: | --: |
| Book profile | 4.000–8.000 | 0,1 |
| Semantic scene audit | 8.000–16.000 | 0,0–0,15 |
| Trinh thám/twist/timeline | 16.000–24.000 | 0,0–0,1 |
| Entity/xưng hô | 4.000–8.000 | 0,0–0,1 |
| Literary Vietnamese | 4.000–10.000 | 0,15–0,30 |
| Red-team | 8.000–16.000 | 0,1 |
| Fix verification | 4.000–8.000 | 0,0 |

Nếu model/account không hỗ trợ thinking config, vẫn đạt cải thiện lớn bằng packet nhỏ, pass đơn mục tiêu, checklist, evidence bắt buộc và red-team.

### Tăng tính chịu trách nhiệm

Ba cơ chế có tác dụng rất mạnh:

1. **Coverage receipt**\
Buộc AI liệt kê hạng mục đã kiểm và 2–5 điểm khó đã đối chiếu.
2. **Evidence-first**\
Không có quote source–target thì không có finding.
3. **Audit challenge**\
Sau pass đầu, một prompt khác yêu cầu model chỉ tìm lỗi bị bỏ sót, không cho khen và không cho lặp nhận xét.

Đây là workflow tốt hơn việc đơn giản yêu cầu “hãy kỹ hơn”, vì “kỹ” là chỉ dẫn mơ hồ.

## Cách tổ chức repo mới

Vì script không audit nội dung, hãy thu gọn code theo hướng **AI audit workstation**:

```text
src/epub_translate_audit/
├── ingest/                 # đọc EPUB, spine, XHTML, metadata
├── segmentation/           # tạo scene/audit packet
├── knowledge/              # nạp glossary, characters, relations, style guide
├── packet_builder/         # chọn context liên quan và render prompt
├── ai/
│   ├── gemini_client.py    # gọi model, cache, retry, thinking config
│   ├── schemas.py          # JSON/Pydantic contract
│   ├── prompts/            # các pass audit
│   ├── orchestrator.py     # gọi pass theo audit plan
│   └── evidence_verify.py  # kiểm quote có tồn tại hay không
├── review/
│   ├── ledger.py           # lưu issue do AI đưa ra
│   ├── red_team.py         # chạy audit đối kháng
│   ├── adjudicate.py       # gộp/khử trùng
│   └── fix_verify.py       # kiểm bản sửa
├── reports/                # XLSX/HTML/Power BI export
└── technical/              # chỉ EPUB validity, mapping, checkpoint
```

Không cần module `rules/` phát hiện semantic/style. Có thể giữ một module `technical/guards` rất hẹp để chặn file hỏng hoặc thiếu chapter, vì đó là integrity, không phải “audit nội dung”.

## Prompt cho Chatbox VS Code

Paste prompt này để đổi hướng codebase hiện có sang AI-led manual audit:

```text
Bạn là principal engineer. Hãy refactor repository `epub-translate-audit` theo mô hình AI-led manual audit.

Yêu cầu kiến trúc:
- AI, không phải scripts, là bên thực hiện audit nội dung song ngữ, consistency, xưng hô, logic, chất văn và localization.
- Scripts chỉ được làm: đọc/tách EPUB, lập packet, nạp knowledge context, gọi Gemini, lưu checkpoint/cache, validate JSON schema, xác minh quote evidence, tạo review queue và report.
- Không được tạo rule engine tự kết luận lỗi dịch, lỗi văn phong, lỗi xưng hô hoặc lỗi cốt truyện.
- Chỉ giữ technical guards không mang tính phán đoán nội dung: EPUB validation, spine integrity, file/chapter missing/duplicate, markup/link/footnote integrity, resume/cache.
- Thay static content rules bằng các AI audit passes: book profiler, audit planner, semantic auditor, continuity auditor, dialogue auditor, literary Vietnamese auditor, localization auditor, red-team auditor, fix verifier.
- Mỗi audit pass dùng packet theo scene/micro-chapter gồm source, target, previous/next context, relevant glossary/entity/relationship/style context.
- Mỗi AI response bắt buộc structured JSON/Pydantic, completed checklist, source/target evidence cho issue, confidence, severity và suggested correction.
- Findings không có quote evidence phải bị evidence verifier loại hoặc retry; không được vào final ledger.
- Implement thinking budget có config theo audit pass khi model hỗ trợ; default semantic audit 12000, red-team 12000, literary 8000.
- Tất cả input EPUB immutable; có checkpoint/resume; không trùng API call khi rerun.
- Cập nhật README, config, prompts, schemas, tests và architecture docs.

Trước tiên:
1. Đọc toàn repo, mô tả những module cần giữ/sửa/xóa.
2. Đưa migration plan ngắn.
3. Sau đó chỉ thực hiện Phase 1: data contracts, AI pass registry, packet schema, prompt templates và evidence verification.
4. Viết tests, chạy tests/lint.
5. Báo cáo file thay đổi, command test, kết quả, giới hạn còn lại.
Không triển khai UI, auto-fix EPUB hoặc gọi API thật ở phase này.
```


## Khuyến nghị thực tế

Flash nên là **workhorse đọc toàn bộ sách**, nhưng không nên là trọng tài duy nhất cho bản thương mại:

- Dùng Flash với packet tốt để audit 100% semantic pass và continuity pass.
- Dùng một pass red-team, có thể cũng là Flash nhưng prompt khác, cho các đoạn high-risk.
- Dùng model reasoning mạnh hơn hoặc human editor cho:
    - Chương mở đầu/kết.
    - Plot twist, lời khai, suy luận, timeline phức tạp.
    - Đoạn cổ văn, thơ, điển cố, câu đối.
    - Cảnh nhiều tầng hàm ý, tâm lý, irony.
    - Những finding Critical/Major mà agent audit không đồng thuận.

Mục tiêu không phải bắt Flash “viết nhận xét dài”; mục tiêu là buộc nó đọc sâu, kiểm tuần tự, nêu bằng chứng và chịu phản biện. Khi packet, pass, context và evidence contract được thiết kế đúng, Flash thường hữu ích hơn rất nhiều so với một prompt audit tổng quát—dù vẫn cần lớp phân xử mạnh hơn cho những đoạn quyết định.

<span style="display:none">[^5_10][^5_11][^5_12][^5_13][^5_14][^5_15][^5_8][^5_9]</span>

<div align="center">⁂</div>

[^5_1]: https://ai.google.dev/gemini-api/docs/prompting-strategies

[^5_2]: https://ai.google.dev/gemini-api/docs/prompting-strategies.md.txt

[^5_3]: https://developers.google.com/ml-kit/genai/prompt/android/prompt-design

[^5_4]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-design-strategies

[^5_5]: https://ai.google.dev/gemini-api/docs/generate-content/thinking

[^5_6]: https://developers.googleblog.com/en/start-building-with-gemini-25-flash/

[^5_7]: https://firebase.google.com/docs/ai-logic/thinking

[^5_8]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/thinking

[^5_9]: https://support.google.com/gemini/thread/339058188/how-do-i-control-thinking-and-thinking-budget-for-gemini-2-5-flash-preview-04-17?hl=en

[^5_10]: https://aclanthology.org/2024.findings-acl.211.pdf

[^5_11]: https://arxiv.org/html/2602.08672v1

[^5_12]: https://www.datastudios.org/post/google-gemini-prompt-engineering-techniques-for-more-accurate-responses

[^5_13]: https://ai.google.dev/gemini-api/docs/structured-output

[^5_14]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/control-generated-output

[^5_15]: https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-structured-outputs/


---

# tôi chỉ yêu cầu audit + path thôi, AI tự động chạy theo pipeline workflows đến khi hoàn thành toàn bộ hệ thống theo tiêu chuẩn

Hiểu đúng yêu cầu của anh/chị: **giao diện người dùng chỉ cần nhập path EPUB bản dịch và bấm Audit**. Từ đó, hệ thống tự tìm EPUB gốc ở folder mẹ, tự phân tích sách, tự lập kế hoạch audit, tự chạy các workflow AI theo nhiều vòng, tự kiểm tra lại bản sửa nếu có, rồi chỉ dừng khi toàn bộ gate đạt chuẩn hoặc trả về danh sách lỗi không thể tự xử lý.

Không cần để người dùng chọn pass, chọn chunk, chọn checklist, chọn model task, hay điều phối thủ công. Toàn bộ phức tạp phải nằm trong orchestration nội bộ.

## Trải nghiệm người dùng cuối

### Input tối giản

```text
EPUB Vietnamese path:
D:\Books\Novel_Project\vi\Novel_VI.epub

[ AUDIT ]
```

Tùy chọn tối thiểu có thể thêm sau:

```text
[ ] Auto-discover source EPUB in parent folder
[ ] Use project knowledge folder if available
[ ] Deep audit mode
[ ] Resume previous unfinished audit
```

Nhưng mặc định, người dùng không phải động đến các tùy chọn này.

### Hành vi sau khi bấm Audit

```text
1. Validate input path
2. Discover source EPUB
3. Validate source and target EPUB
4. Extract structure from both EPUBs
5. Align source ↔ target
6. Profile book automatically
7. Create adaptive audit plan
8. Build knowledge base automatically
9. Run AI audit workflows
10. Red-team all high-risk or uncertain content
11. Adjudicate and verify evidence
12. Run release gates
13. Generate report and review queue
14. Stop only at PASS, CONDITIONAL PASS, or FAIL
```

Người dùng chỉ nhận một trạng thái cuối:


| Trạng thái | Ý nghĩa |
| :-- | :-- |
| `PASS` | Đạt chuẩn phát hành theo policy; không còn blocker |
| `CONDITIONAL_PASS` | Không còn blocker, chỉ còn lỗi Minor/Cosmetic trong error budget |
| `REVIEW_REQUIRED` | Không thể kết luận tự động vì source/target mơ hồ, confidence thấp hoặc cần quyết định editorial |
| `FAIL` | Có lỗi chặn phát hành: EPUB hỏng, thiếu nội dung, Critical/Major chưa giải quyết, consistency lỗi nặng |
| `PARTIAL` | Workflow bị gián đoạn hoặc API lỗi vượt retry; có thể `--resume` mà không chạy lại phần đã hoàn thành |

## Pipeline tự động hoàn chỉnh

```text
User enters translated EPUB path
             │
             ▼
┌──────────────────────────────┐
│ 0. Intake and discovery      │
│ - validate path              │
│ - find source in parent      │
│ - discover knowledge folder  │
│ - create immutable run       │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 1. EPUB preparation          │
│ - validate source/target     │
│ - unpack to work folder      │
│ - read OPF, spine, nav       │
│ - extract metadata/XHTML     │
│ - preserve IDs and anchors   │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 2. Source-target mapping     │
│ - map part and chapter       │
│ - map blocks and scenes      │
│ - construct audit packets    │
│ - send uncertain pairs to AI │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 3. AI book understanding     │
│ - infer genre/register       │
│ - identify story risks       │
│ - extract key entities       │
│ - extract relations/voice    │
│ - derive audit strategy      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 4. AI-led manual audit       │
│ - semantic accuracy          │
│ - completeness and references│
│ - dialogue and address       │
│ - terminology/entities       │
│ - literary Vietnamese        │
│ - culture/localization       │
│ - continuity per arc         │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 5. Adversarial verification  │
│ - red-team high-risk content │
│ - check evidence quotes      │
│ - resolve agent disagreement │
│ - deduplicate findings       │
│ - detect systemic defects    │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 6. Completion loop           │
│ - classify remaining issues  │
│ - create correction queue    │
│ - re-audit corrected areas   │
│ - continue until stable      │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│ 7. Release gate              │
│ - technical integrity        │
│ - semantic safety            │
│ - consistency                │
│ - literary acceptance        │
│ - coverage and sign-off      │
└──────────────┬───────────────┘
               ▼
      Report / PASS / FAIL
```

Các tài liệu Gemini khuyến nghị dùng instruction cụ thể, phân tách context rõ bằng delimiters, chia bài toán phức tạp thành các nhiệm vụ tập trung, và dùng structured output khi cần pipeline xử lý kết quả tin cậy. Đây là cơ sở để biến một model Flash thành các “vai trò audit” hẹp nhưng có thể chạy tự động tuần tự.[^6_1][^6_2][^6_3]

## Orchestrator phải tự quyết gì

Người dùng không chọn workflow; `AuditOrchestrator` tự chọn dựa trên thông tin thực tế từ sách.


| Dấu hiệu tự phát hiện | Workflow được kích hoạt/tăng cường |
| :-- | :-- |
| Nhiều thoại, nhiều người nói | Dialogue, speaker attribution, xưng hô, relationship drift |
| Trinh thám/điều tra | Evidence chain, causality, timeline, ambiguity, spoiler control |
| Tiên hiệp/huyền huyễn | Cảnh giới, công pháp, hệ thống sức mạnh, danh xưng, phe phái |
| Cổ đại/lịch sử | Tước vị, lễ nghi, register cổ phong, điển cố, lịch pháp |
| Romance/BL/GL | Subtext, intimacy register, consent-sensitive language, relationship progression |
| Kinh dị/tâm lý | Narrative tension, unreliable narration, ambiguity, emotional gradient |
| Sci-fi/fantasy | Worldbuilding, invented terminology, capability/rule consistency |
| Sách kỹ thuật/phi hư cấu | Số liệu, bảng, trích dẫn, thuật ngữ kỹ thuật, mệnh đề điều kiện |
| Alignment confidence thấp | AI alignment review và completeness audit 100% |
| Nhiều error lặp cùng pattern | Root-cause workflow, mở rộng scope audit trên toàn corpus |
| Critical/Major issue | Red-team bắt buộc ở scene và context lân cận |
| AI agents bất đồng | Adjudication workflow, escalation lên reviewer mạnh hơn hoặc human queue |

Nguyên tắc: planner được quyền **tăng** độ sâu và phạm vi audit, nhưng không được tự giảm các phần audit bắt buộc.

## Chu trình “tự chạy đến hoàn thành”

Cần định nghĩa kỹ “hoàn thành”. Hệ thống không nên vô hạn loop vì AI có thể liên tục tìm lỗi cosmetic.

### Completion contract

```yaml
completion:
  maximum_workflow_rounds: 4
  maximum_red_team_rounds_per_packet: 2
  no_new_material_issues_for_consecutive_rounds: 2
  recheck_after_major_or_critical: true
  recheck_context_before_after_segments: 2
  allow_auto_rewrite: false
  require_final_stability_pass: true
```

Điều kiện kết thúc:

1. Toàn bộ EPUB source và target được ingest/validate thành công.
2. 100% chapter/block có trạng thái mapped hoặc được giải trình rõ.
3. 100% packet high-risk đã được semantic audit và red-team.
4. Baseline coverage theo policy đã hoàn tất.
5. Mọi issue AI phải qua Pydantic validation và evidence verification.
6. Issue trùng đã được gộp; systemic issue được phân loại.
7. Không phát hiện thêm lỗi Critical/Major mới qua 2 lượt stability pass liên tiếp.
8. Các hard-block release gate không còn blocker.
9. Báo cáo và artifact cuối đã được tạo thành công.

Nếu có lỗi cần biên tập con người sửa, hệ thống phải dừng ở `REVIEW_REQUIRED`, không giả vờ rằng “AI sẽ tự hoàn thành”. Nếu anh/chị muốn AI tự sửa EPUB, đó là một workflow khác và phải tạo **bản sửa mới**, diff rõ từng thay đổi, rồi audit lại từ đầu các vùng bị ảnh hưởng.

## Auto-discovery convention

Để user chỉ nhập một path, tool nên dùng convention rõ ràng nhưng có cơ chế fallback an toàn:

```text
Project/
├── original.epub
├── vi/
│   └── translated_vi.epub    ← user nhập path này
├── knowledge/                ← tự đọc nếu tồn tại
│   ├── glossary.csv
│   ├── entities.json
│   ├── relationships.json
│   ├── style_guide.md
│   └── editorial_policy.md
└── audit-output/             ← tự tạo
```

Logic:

```text
translated = user path
parent = translated.parent

source candidates:
  1. parent/*.epub (trừ translated)
  2. parent.parent/*.epub (trừ translated)
  3. file tên gần nhất với translated nhưng không mang suffix _vi/_vn/_viet
  4. EPUB có metadata language khác vi

knowledge candidates:
  1. parent/knowledge/
  2. parent.parent/knowledge/
  3. parent/.audit/knowledge/
  4. files có tên glossary, entity, character, relationship, style, policy
```

Nếu source không duy nhất, tool không được “chọn bừa”. Nhưng để giữ UX một-input, UI/CLI có thể hiển thị lựa chọn ngắn:

```text
Found 3 possible source EPUB files:
[^6_1] Novel_original.epub
[^6_2] Novel_raw.epub
[^6_3] Novel_old_revision.epub

Select source [1-3]:
```

Đây vẫn là một workflow tối giản, nhưng bảo vệ audit khỏi map nhầm source.

## Prompt giao Chatbox để xây đúng hướng

Đây là prompt nên paste vào Chatbox ở VS Code. Nó thay thế toàn bộ cách tiếp cận nhiều flag/pass của người dùng bằng một lệnh duy nhất.

```text
Bạn là principal engineer xây dựng tool production-ready `epub-translate-audit`.

Mục tiêu trải nghiệm người dùng:
- Người dùng chỉ cung cấp DUY NHẤT đường dẫn EPUB bản dịch tiếng Việt.
- Lệnh duy nhất là:
  epub-audit audit "<translated_epub_path>"
- Hệ thống tự discover EPUB gốc từ folder mẹ hoặc folder mẹ cao hơn 1 cấp.
- Hệ thống tự discover knowledge folder nếu có.
- Người dùng không chọn audit pass, chunk size, genre, workflow, model task, threshold hay sampling strategy.
- Hệ thống tự điều phối toàn bộ workflow đến khi đạt completion contract hoặc dừng an toàn ở REVIEW_REQUIRED/FAIL/PARTIAL.
- Không auto sửa EPUB ở phase này. Chỉ audit, sinh report và queue sửa.

Kiến trúc bắt buộc:
1. Script không được tự kết luận lỗi dịch, lỗi văn phong, lỗi xưng hô, lỗi logic hay lỗi consistency nội dung.
2. AI là auditor chính: book profiler, audit planner, semantic auditor, continuity auditor, dialogue auditor, literary Vietnamese auditor, localization auditor, red-team auditor, adjudicator, fix verifier.
3. Script chỉ làm operational plumbing:
   - validate path và EPUB integrity;
   - discover source EPUB và knowledge;
   - extract theo OPF spine;
   - tách part/chapter/scene/audit packet;
   - build source-target context packet;
   - gọi Gemini Flash;
   - structured-output/Pydantic validation;
   - verify quote evidence;
   - cache/checkpoint/resume/rate limit;
   - lưu ledger/report/review queue;
   - technical guards cho missing chapter/markup/nav/footnote.
4. AI planner tự nhận diện thể loại, register, density thoại, worldbuilding, rủi ro logic và tự chọn/tăng workflow cần chạy.
5. Planner không được tắt các workflow mandatory: semantic accuracy, completeness, entity/terminology, continuity, dialogue, literary Vietnamese, localization, red-team high-risk.
6. Mỗi AI pass dùng scene/micro-chapter packet gồm source, Vietnamese target, context trước/sau và knowledge liên quan.
7. Tất cả AI findings cần source evidence + target evidence + category + severity + confidence + explanation + impact + suggested correction.
8. Finding không đủ Pydantic schema hoặc quote evidence không tồn tại trong packet thì retry một lần; vẫn lỗi thì reject, log, không đưa vào final ledger.
9. Gemini Flash được gọi với structured JSON; thinking budget config tự chọn theo pass, nhưng có fallback nếu model không hỗ trợ.
10. Không sửa input EPUB. Có immutable run directory, content hash, SQLite state, idempotency, resume và cache.
11. Workflow completion phải có tối đa rounds, stability condition và release gate rõ ràng. Không loop vô hạn vì cosmetic issues.
12. Status cuối chỉ là PASS, CONDITIONAL_PASS, REVIEW_REQUIRED, FAIL, PARTIAL. RELEASED yêu cầu human command riêng.

Hãy thực hiện theo thứ tự:
PHASE 1:
- Khảo sát repository hiện tại.
- Tạo/điều chỉnh CLI để hỗ trợ duy nhất command `epub-audit audit "<path>"`.
- Implement input discovery, run state, status state machine, completion contract, skeleton AI pass registry.
- Viết config internal defaults; user không phải truyền config cho flow mặc định.
- Viết tests cho source discovery, ambiguous source handling, run resume, state transition và completion stopping conditions.
- Không gọi API Gemini thật trong phase này; mock client.
- Cập nhật README với user workflow một lệnh.

Sau khi hoàn tất:
- Chạy tests/lint.
- Báo cáo chính xác file tạo/sửa.
- Nêu command đã chạy và kết quả.
- Nêu các phase còn lại.
Không commit, push hoặc xóa file nếu tôi chưa yêu cầu.
```


## CLI cuối cùng nên như thế nào

Người dùng chỉ cần biết hai lệnh:

```powershell
# Chạy audit mới
epub-audit audit "D:\Books\Project\vi\translated.epub"

# Tiếp tục một lần chạy bị gián đoạn
epub-audit resume "D:\Books\Project\audit-output\run-20260903-082300"
```

Các option khác vẫn tồn tại nội bộ cho developer/debugging, nhưng không cần xuất hiện trong hướng dẫn dùng hàng ngày.

```powershell
epub-audit audit "D:\Books\Project\vi\translated.epub" `
  --deep `
  --resume
```

`--deep` chỉ nên là một lựa chọn đơn giản nếu anh/chị thực sự muốn phân biệt mức chi phí/thời gian; còn mặc định nên dùng `standard` adaptive audit.

## Những gì AI tự làm vs. không tự làm

| Hệ thống tự làm đến cùng | Hệ thống phải dừng/chờ |
| :-- | :-- |
| Đọc EPUB, map source–target, chia packet | Không tìm được source EPUB duy nhất |
| Nhận diện thể loại và lập audit plan | EPUB source hỏng hoặc không đọc được |
| Audit nghĩa, văn phong, xưng hô, thuật ngữ | Alignment mơ hồ không đủ evidence để kết luận |
| Chạy red-team và adjudication | Cần quyết định editorial policy còn thiếu |
| Phân loại lỗi, severity, CAPA | Lỗi Major/Critical không thể giải quyết vì cần biên tập |
| Tạo report, XLSX, Power BI datasets | Phát hành chính thức nếu policy yêu cầu human sign-off |
| Resume sau API/network failure | Xác nhận quyền gửi nội dung sách lên cloud API nếu policy yêu cầu |

Tóm lại, yêu cầu “chỉ audit + path” là hoàn toàn đúng ở tầng UX. Nhưng bên trong vẫn cần workflow nhiều lớp để Flash không làm việc hời hợt: **AI planner → audit chuyên vai → red-team → evidence verifier → adjudicator → release gate**. Model không được quyền tự tuyên bố “hoàn thành” chỉ sau một lượt đọc; chỉ orchestrator, dựa trên coverage và completion contract, mới được phép kết thúc job.

<span style="display:none">[^6_4][^6_5][^6_6]</span>

<div align="center">⁂</div>

[^6_1]: https://ai.google.dev/gemini-api/docs/prompting-strategies

[^6_2]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-design-strategies

[^6_3]: https://ai.google.dev/gemini-api/docs/structured-output

[^6_4]: image.jpg

[^6_5]: interests.ai_translation

[^6_6]: preferences.prompt_customization.translation_workflow

