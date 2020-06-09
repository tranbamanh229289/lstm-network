# Cách sử dụng code của tôi : 
## Clone respond của tôi về 
## Mở conda prompt tạo môi trường :conda env create -n new_name_env -f=\path\to\env.yml
## Kích hoạt môi trường vừa tạo , chạy file LSTM.py
# Xử lí dữ liệu 
## Vì dữ liệu đầu vào là chuỗi thời gian nên trước tiên muốn phân tích hồi quy liên quan tới chuỗi thời gian thì đòi hỏi các chuỗi dữ liệu đó là chuỗi dừng (stationary).Nên bước đầu tiên tôi sẽ chuyển chuỗi dữ liệu trở thành chuỗi dừng 

## Theo mô hình LSTM .Đầu vào mô hình là điểm dữ liệu x(i) sẽ dự đoán đầu ra là điểm dữ liệu x(i+1) .Tức là nhãn của điểm dữ liệu x(i) sẽ là điểm dữ liệu x(i+1).Ta chuyển dữ liệu của chuỗi dừng về dữ liệu của bài toán học tập có giám sát 

## Khi một vector đi qua mạng neuron, chúng trải qua rất nhiều phép tính và trong quá trình đó sẽ có thành phần nào đó trở nên quá to và khiến các thành phần khác trở nên không đáng kể. Hàm tanh lúc này. sẽ giúp tinh chỉnh sự chênh lệch này để giúp "các thành phần yếu thế vẫn có tiếng nói trong xã hội".Vậy chúng ta sẽ chuyển các giá trị của bài toán học có giám sát trong khoảng (-1,1) bằng hàm tanh .Nhưng ở đây tôi sẽ dùng lớp Minmaxscaler trong thư viện sklearn để chuyển dữ liệu trong khoảng (-1,1)

## Sau khi chuẩn bị dữ liệu xong ta sẽ chia dữ liệu thành tập test và train , tổng cộng dataset có 36 điểm dữ liệu liên tiếp , ta sẽ chia tập train có 24 điểm dữ liệu liên tiếp (chuỗi thời gian ) và tập test có 12 điểm dữ liệu liên tiếp (chuỗi thời gian )

# Training
## Đưa tập train vào training ra model . Hàm loss là hàm MSE , Thuật toán tối ưu ADAM .Thuật toán này cho các weight ban đầu random nên sẽ cho ra các dự đoán các kết quả hàm loss khác nhau .Các kết quả này gọi là các cực tiểu địa phương .

## Lấy model đó dự đoán cho tập test .Dự đoán xong ta sẽ có các hàm inverse để đưa các giá trị dự đoán về dạng chuỗi thời gian ban đầu 

## Giá trị là RMSE là giá trị độ lệch giữa predict và giá trị mong đợi 
