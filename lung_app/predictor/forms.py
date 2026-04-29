from django import forms

YES_NO_CHOICES = [
    (1, "1"),
    (2, "2"),
]

GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
]

class LungCancerForm(forms.Form):
    GENDER = forms.ChoiceField(choices=GENDER_CHOICES)
    AGE = forms.IntegerField(min_value=1, max_value=120)

    SMOKING = forms.ChoiceField(choices=YES_NO_CHOICES)
    YELLOW_FINGERS = forms.ChoiceField(choices=YES_NO_CHOICES)
    ANXIETY = forms.ChoiceField(choices=YES_NO_CHOICES)
    PEER_PRESSURE = forms.ChoiceField(choices=YES_NO_CHOICES)
    CHRONIC_DISEASE = forms.ChoiceField(label="CHRONIC DISEASE", choices=YES_NO_CHOICES)
    FATIGUE = forms.ChoiceField(choices=YES_NO_CHOICES)
    ALLERGY = forms.ChoiceField(choices=YES_NO_CHOICES)
    WHEEZING = forms.ChoiceField(choices=YES_NO_CHOICES)
    ALCOHOL_CONSUMING = forms.ChoiceField(label="ALCOHOL CONSUMING", choices=YES_NO_CHOICES)
    COUGHING = forms.ChoiceField(choices=YES_NO_CHOICES)
    SHORTNESS_OF_BREATH = forms.ChoiceField(label="SHORTNESS OF BREATH", choices=YES_NO_CHOICES)
    SWALLOWING_DIFFICULTY = forms.ChoiceField(label="SWALLOWING DIFFICULTY", choices=YES_NO_CHOICES)
    CHEST_PAIN = forms.ChoiceField(label="CHEST PAIN", choices=YES_NO_CHOICES)

    def cleaned_feature_dict(self):
        data = self.cleaned_data
        return {
            "GENDER": data["GENDER"],
            "AGE": int(data["AGE"]),
            "SMOKING": int(data["SMOKING"]),
            "YELLOW_FINGERS": int(data["YELLOW_FINGERS"]),
            "ANXIETY": int(data["ANXIETY"]),
            "PEER_PRESSURE": int(data["PEER_PRESSURE"]),
            "CHRONIC DISEASE": int(data["CHRONIC_DISEASE"]),
            "FATIGUE": int(data["FATIGUE"]),
            "ALLERGY": int(data["ALLERGY"]),
            "WHEEZING": int(data["WHEEZING"]),
            "ALCOHOL CONSUMING": int(data["ALCOHOL_CONSUMING"]),
            "COUGHING": int(data["COUGHING"]),
            "SHORTNESS OF BREATH": int(data["SHORTNESS_OF_BREATH"]),
            "SWALLOWING DIFFICULTY": int(data["SWALLOWING_DIFFICULTY"]),
            "CHEST PAIN": int(data["CHEST_PAIN"]),
        }
