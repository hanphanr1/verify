# Sample Veteran Data Formats

## Format 1: BIRLS / VA Records (JSON)
```json
{
  "firstName": "John",
  "lastName": "Smith",
  "dateOfBirth": "1985-03-15",
  "ssnLast4": "1234",
  "branch": "Army",
  "serviceStartDate": "2010-06-01",
  "serviceEndDate": "2018-05-31",
  "characterOfDischarge": "Honorable",
  "vaBenefitTypes": ["healthcare", "gi_bill", "disability"]
}
```

## Format 2: DD-214 (JSON)
```json
{
  "fullName": "John Michael Smith",
  "firstName": "John",
  "middleName": "Michael",
  "lastName": "Smith",
  "dateOfBirth": "1985-03-15",
  "ssn": "123-45-6789",
  "branch": "US Army",
  "grade": "E-4",
  "mos": "11B",  // Military Occupational Specialty
  "dateEnteredActiveDuty": "2010-06-01",
  "dateOfDischarge": "2018-05-31",
  "characterOfService": "Honorable",
  "decorations": ["Army Commendation Medal", "Afghanistan Campaign Medal"],
  "separationStation": "Fort Hood, TX"
}
```

## Format 3: SheerID API (JSON)
```json
{
  "programId": "MILITARY_PROGRAM_ID",
  "metadata": {
    "firstName": "John",
    "lastName": "Smith",
    "birthDate": "1985-03-15",
    "email": "john.smith@email.com"
  }
}
```

```json
{
  "verificationId": "abc123-xyz789",
  "status": "VETERAN",
  "firstName": "John",
  "lastName": "Smith",
  "birthDate": "1985-03-15",
  "email": "john.smith@email.com",
  "organization": "4070",
  "dischargeDate": "2018-05-31",
  "country": "US",
  "locale": "en-US",
  "consent": true
}
```

## Format 4: CSV Template (BIRLS/VA)
```csv
first_name,last_name,date_of_birth,ssn_last4,branch,service_start,service_end,discharge_type
John,Smith,1985-03-15,1234,Army,2010-06-01,2018-05-31,Honorable
Jane,Doe,1990-07-22,5678,Navy,2012-01-15,2019-12-20,Honorable
Michael,Johnson,1988-11-08,9012,Air Force,2008-09-01,2016-08-15,General
```

## Format 5: Telegram Bot Input
```
Họ tên: John Smith
Ngày sinh: 1985-03-15
Email: john.smith@email.com
Quân binh chủng: Army
Ngày xuất ngũ: 2018-05-31
```

---

## Military Branch Codes (SheerID/DMDC)
| Code | Branch |
|------|--------|
| 4070 | Army |
| 4071 | Marine Corps |
| 4072 | Navy |
| 4073 | Air Force |
| 4074 | Coast Guard |
| 4544268 | Space Force |

## Character of Discharge
- Honorable
- General (Under Honorable Conditions)
- Other Than Honorable
- Bad Conduct
- Dishonorable
