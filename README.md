# 📝 การติดตั้งโปรแกรม


## 📌 สิ่งที่จำเป็น
1. `python` (แนะนำเวอร์ชัน 3.9.4)
2. `venv` module (เครื่องมือสำหรับการสร้าง virtual environments บน python)

![](https://i.imgur.com/waxVImv.png)

## ⚙️ ขั้นตอนการติดตั้งโปรแกรม
1. สร้าง `Environment` สำหรับโปรแกรม

        python -m venv .env

2. เข้าถึง `Environment` ด้วยคำสั่ง ดังนี้

    - สำหรับ Windows (`PowerShell`)

            .env\Scripts\Activate.ps1

    - สำหรับ Windows (`Command Prompt` หรือ `CMD`)

            .env\Scripts\activate.bat

    - สำหรับ `Linux` หรือ `MacOS`

            .env/Scripts/activate

3. ติดตั้ง `Python Packages` ที่จำเป็น
        
        python -m pip install -r requirements.txt

4. ตรวจสอบ `USB Port` สำหรับรับข้อมูล แก้ไข COM Port ดังภาพ 

    - เปิดไฟล์ `./python/genMat32-calibrated.py บรรทัดที่ 17`  ( [เปิด](./python/genMat32-calibrated.py#L17) )

    - ภาพตัวอย่างการแก้ไข COM Port

        ![](./port.JPG "ตรวจสอบ USB Port สำหรับรับข้อมูล")


5. `รันโปรแกรม` โดยต้องการรัน 2 ส่วนพร้อมกัน

    - สำหรับ `เว็บแอปพลิเคชัน`

                cd dashboard
                python app.py

    - สำหรับ `รับข้อมูลจากอุปกรณ์วัดแรงกดทับ`
    
                cd python 
                python genMat32-calibrated.py

![](https://i.imgur.com/waxVImv.png)