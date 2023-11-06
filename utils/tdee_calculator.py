def calculate_tdee(gender, age, weight, height, activity_level):
    # Harris-Benedict Formula for BMR Calculation
    # https://www.omnicalculator.com/health/bmr-harris-benedict-equation

    if gender == "Male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == "Female":
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    activity_factors = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "extra_active": 1.9
    }

    tdee = bmr * activity_factors[activity_level]

    return tdee

def calculate_macros(target_calories, protein_percentage=0.30, fat_percentage=0.35, carb_percentage=0.35):
    protein_calories = target_calories * protein_percentage
    fat_calories = target_calories * fat_percentage
    carb_calories = target_calories * carb_percentage

    # 1 gram protein = 4 kalori, 1 gram lemak = 9 kalori, 1 gram karbohidrat = 4 kalori
    protein_grams = protein_calories / 4
    fat_grams = fat_calories / 9
    carb_grams = carb_calories / 4

    return protein_grams, fat_grams, carb_grams
