# US Veteran Verification Data Sources

## 1. BIRLS (Beneficiary Identification and Records Locator)

**Nguồn**: https://www.birls.org (thông qua Reclaim The Records)

**Dữ liệu**:
- ~19.5 triệu veterans đã nhận VA benefits
- Thông tin về: health care, disability, GI Bill, VA loans
- Các binh chủng: Army, Navy, Air Force, Marine Corps, Coast Guard, Space Force
- Bao gồm cả Women Army Corps (WACs), Army Air Corps (defunct)
- Một số Philippine Commonwealth Army veterans

**Miễn phí**: Có - được public qua FOIA lawsuit

**Cập nhật**:
- Tháng 12/2024: Ban đầu publish
- Tháng 9/2025: Thêm 1.5 triệu records (2020-2023)

**Cách truy cập**:
- ReclaimTheRecords.org có index searchable
- Data được tổng hợp từ VA benefits records

---

## 2. DD-214 (Giấy xuất ngũ / Discharge Document)

**Nguồn chính**:
- https://vetrecs.archives.gov (National Archives - eVetRecs)
- milConnect.dmdc.mil

**Yêu cầu**:
- Cần xác minh identity qua ID.me
- Cần biết thông tin cơ bản để request

**Lưu trữ theo thời gian**:
- Navy: sau 1995
- Army: sau 2002
- Marine Corps: sau 1999
- Air Force: sau 2004
- Các records cũ hơn có thể đã chuyển sang National Archives

**Thông tin trên DD-214**:
- Họ tên đầy đủ
- Ngày sinh
- Social Security Number
- Ngày nhập ngũ / xuất ngũ
- Character of discharge (Honorable, General, Dishonorable, etc.)
- Military occupational specialty (MOS)
- Awards and decorations

---

## 3. DMDC (Defense Manpower Data Center)

**Truy cập**: milconnect.dmdc.mil

**Dữ liệu**:
- Active duty personnel
- Reserve forces
- Veterans đã được Defense Department records
- Service members đang trong hệ thống DEERS

**Đặc điểm**:
- Database chính thức của Department of Defense
- Truy cập cần login (DS Logon, CAC card, hoặc ID.me)

---

## 4. SheerID

**Website**: https://www.sheerid.com

**Đặc điểm**:
- Commercial verification service
- Sử dụng 200K+ authoritative data sources
- API sẵn có cho developers
- Hỗ trợ nhiều loại verification: Student, Teacher, Military, Healthcare, First Responder, etc.

**API Flow**:
```
1. POST /verification/ - Tạo verification request
2. POST /verification/{id}/step/collectMilitaryStatus - Gửi military status (VETERAN, ACTIVE_DUTY, etc.)
3. POST /verification/{id}/step/collectInactiveMilitaryPersonalInfo - Gửi personal info
4. GET /verification/{id} - Check status
```

**Military Branch Codes**:
- 4070: Army
- 4071: Marine Corps
- 4072: Navy
- 4073: Air Force
- 4074: Coast Guard
- 4544268: Space Force

---

## So sánh các nguồn

| Nguồn | Loại | Miễn phí | API | Độ chính xác |
|-------|------|----------|-----|--------------|
| BIRLS | VA Benefits Records | ✅ | ❌ | Cao |
| DD-214 | Discharge Records | ✅ (có limit) | ❌ | Rất cao |
| DMDC | DoD Records | Cần đăng nhập | ✅ (hạn chế) | Rất cao |
| SheerID | Commercial Service | ❌ (trả phí) | ✅ | Cao |

---

## Khuyến nghị

1. **Cho verification thương mại**: Dùng SheerID API (đã tích hợp sẵn, đáng tin cậy)
2. **Cho research/genealogy**: BIRLS data từ ReclaimTheRecords
3. **Cho xác minh chính chủ**: Kết hợp DD-214 + ID.me verification

---

## Các field thường dùng để verify

### BIRLS Fields:
- First Name
- Last Name
- Date of Birth
- Social Security Number (last 4 digits thường đủ để match)
- Branch of Service
- Service Period (start/end dates)
- Character of Discharge

### DD-214 Fields:
- Full Name
- Date of Birth
- SSN
- Date Entered Active Duty
- Date of Discharge
- Character of Service
- Branch
- MOS (Military Occupational Specialty)
- Decorations/Awards

### SheerID API Parameters:
```json
{
  "programId": "...",
  "metadata": {
    "firstName": "...",
    "lastName": "...",
    "birthDate": "YYYY-MM-DD",
    "email": "..."
  }
}
```

```json
{
  "status": "VETERAN",  // hoặc ACTIVE_DUTY, RESERVE, NATIONAL_GUARD
  "firstName": "...",
  "lastName": "...",
  "birthDate": "YYYY-MM-DD",
  "email": "...",
  "organization": "4070",  // branch code
  "dischargeDate": "YYYY-MM-DD",
  "country": "US",
  "locale": "en-US",
  "consent": true
}
```
