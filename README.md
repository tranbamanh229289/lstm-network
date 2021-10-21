# Cách sử dụng code của tôi : 
* Clone respond của tôi về 
* Mở conda prompt tạo môi trường :conda env create -n new_name_env -f=\path\to\env.yml
* Kích hoạt môi trường vừa tạo , chạy file LSTM.py
* Xử lí dữ liệu 
* Vì dữ liệu đầu vào là chuỗi thời gian nên trước tiên muốn phân tích hồi quy liên quan tới chuỗi thời gian thì đòi hỏi các chuỗi dữ liệu đó là chuỗi dừng (stationary).Nên bước đầu tiên tôi sẽ chuyển chuỗi dữ liệu trở thành chuỗi dừng 

* Theo mô hình LSTM .Đầu vào mô hình là điểm dữ liệu x(i) sẽ dự đoán đầu ra là điểm dữ liệu x(i+1) .Tức là nhãn của điểm dữ liệu x(i) sẽ là điểm dữ liệu x(i+1).Ta chuyển dữ liệu của chuỗi dừng về dữ liệu của bài toán học tập có giám sát 

* Trong các thuật toán machine learning nói chung , việc feature scaling là cần thiết để điều chỉnh độ giãn cách giữa các giá trị .Một thuật toán sẽ hoạt động không tốt nếu các thuộc tính trong dữ liệu có độ dãn cách quá khác nhau ,ví dụ đầu vào là mảng [[1],[1000]].Vậy thì giá trị [1] sẽ bị coi nhẹ tầm quan trọng, giá trị 1 quá nhỏ so với 1000 nên giá trị 1 sẽ k gây được ảnh hưởng vào model trong quá trình training .Để giảm thiểu tình trạng này , người ta sẽ điều chỉnh độ giãn cách giữa 2 giá trị này thu hẹp lại giúp cho những giá trị nhỏ cũng giống như giúp tầng lớp vô sản có tiếng nói và làm chủ hơn trong xã hội .

* Hơn nữa Vì trong mạng Neuron của chúng ta có các hàm Sigmoid và Tanh cho các giá trị trong khoảng (0,1) và (-1,1) nên việc chuẩn hóa dữ liệu đầu vào là cần thiết,giúp cho tốc độ tối ưu được nhanh hơn,chúng ta có thể nhìn thấy đồ thị đạo hàm hàm sigmoid , hàm này sẽ cho giá trị lớn nhất trong khoảng x từ (-1,1) và x càng lớn vô cùng thì giá trị đạo hàm càng bé . Mà khi dùng thuật toán gradient descent và ADAM thì đạo hàm lớn sẽ cho tốc độ hội tụ cực tiểu địa phương nhanh hơn.Vì vậy trong các kiến trúc mạng có hàm sigmoid và tanh , chúng ta nên chuẩn hóa dữ liệu trong khoảng (-1,1) để tối ưu hóa quá trình tối ưu .Ở đây tôi chuẩn hóa dữ liệu đầu vào trong khoảng từ (-1,1) .Có 2 cách để transform là normalization và  standardization.Ở đây Tôi sử dụng Normalization bằng lớp MinmaxScaler trong thư viện Sklearn.

* Sau khi chuẩn bị dữ liệu xong ta sẽ chia dữ liệu thành tập test và train , tổng cộng dataset có 36 điểm dữ liệu liên tiếp , ta sẽ chia tập train có 24 điểm dữ liệu liên tiếp (chuỗi thời gian ) và tập test có 12 điểm dữ liệu liên tiếp (chuỗi thời gian )

# Training
* Đưa tập train vào training ra model . Hàm loss là hàm MSE , Thuật toán tối ưu ADAM .Thuật toán này cho các weight ban đầu random nên sẽ cho ra các dự đoán các kết quả hàm loss khác nhau .Các kết quả này gọi là các cực tiểu địa phương .

* Lấy model đó dự đoán cho tập test .Dự đoán xong ta sẽ có các hàm inverse để đưa các giá trị dự đoán về dạng chuỗi thời gian ban đầu. 

* Giá trị là RMSE là giá trị độ lệch giữa predict và giá trị mong đợi .
