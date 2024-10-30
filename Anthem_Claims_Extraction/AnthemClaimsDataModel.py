from pydantic import BaseModel

class AnthemClaimsChildColumns(BaseModel):
    Month = "Month"
    MedicalSubscribers = "Medical Subscribers"
    MedicalMembers = "'Medical Members"
    PharmacySubscribers = "Pharmacy Subscribers"
    PharmacyMembers = "Pharmacy Members"
    MedicalPaidPMPM = "Medical PaidPMPM"
    MedicalPaidPEPM = "Medical PaidPEPM"
    PharmacyPaidPMPM = "Pharmacy PaidPMPM"
    PharmacyPaidPEPM = "Pharmacy PaidPEPM"
    TotalMedical = "Total Medical"
    TotalPharmacy = "Total Pharmacy"
    TotalPaidAmount = "Total PaidAmount"

class AnthemClaimsParentColumns(BaseModel):
    MemberMonths = "'Member Months"
    PaidAmounts = "Paid Amounts"