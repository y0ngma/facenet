import cv2, os

img_last = None # 이전 프레임을 저장할 변수
no = 0 # 이미지 장 수 
save_dir = "./extract" # 저장 디렉터리 이름
os.mkdir(save_dir) # 디렉터리 만들기

cap = cv2.VideoCapture('test.m4v') # 동영상파일로부터 입력받기
while True:
    is_ok, frame = cap.read() # 이미지 추출
    if not is_ok: break
    frame = cv2.resize(frame, (640,360))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY ) # 흑백변환
    gray = cv2.GaussianBlur(gray, (15,15), 0)
    img_b = cv2.threshold( gray, 127, 255, cv2.THRESH_BINARY )[1]
    
    if not img_last is None:
        frame_diff = cv2.absdiff( img_last, img_b ) # 이전프레임과 차이반환
        contours = cv2.findContours(frame_diff,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE )[1]

        for contour in contours: # 차이가 있는부분 파일로 출력
            x,y,w,h = cv2.boundingRect(contour)
            if w < 100 or w > 500: continue # 노이즈제거
            imgex = frame[y:y+h, x:x+w]
            outfile = save_dir + '/' + str(no) + '.jpg'
            cv2.imwrite(outfile, imgex)
            no += 1
    img_last = img_b
cap.release()
print('ok')