import pyttsx3
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import keyboard

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text, lang="ar"):
    engine.setProperty("rate", 150)

    if lang == "ar":
        engine.setProperty("voice", "com.apple.speech.synthesis.voice.tarik")
    elif lang == "fr":
        engine.setProperty("voice", "com.apple.speech.synthesis.voice.thomas")
    else:
        engine.setProperty("voice", "com.apple.speech.synthesis.voice.tarik")

    engine.say(text)
    engine.runAndWait()

def listen(language="ar"):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        if language == "ar":
            speak("في انتظار أمرك.")
        elif language == "fr":
            speak("En attente de votre commande.")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio, language=language)
            return user_input.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            if language == "ar":
                speak("عذرًا، لم أستطع فهم طلبك.")
            elif language == "fr":
                speak("Désolé, je n'ai pas pu comprendre votre demande.")
            return ""

def launch_program(commands):
    browser = webdriver.Chrome()
    lang = "ar"  # Default to Arabic

    while True:
        user_command = listen(language=lang)
        if "إغلاق" in user_command or "fermer" in user_command:
            speak("إغلاق البرنامج.", lang=lang)
            break
        elif "changer la langue" in user_command or "changer de langue" in user_command:
            lang = toggle_language(lang)
        else:
            handle_command(user_command, browser, commands, lang)

    browser.quit()

def toggle_language(current_lang):
    if current_lang == "ar":
        speak("Passage au français.", lang="fr")
        return "fr"
    else:
        speak("تبديل إلى اللغة العربية.", lang="ar")
        return "ar"

def handle_command(user_command, browser, commands, lang):
    for command, handler in commands.items():
        if command in user_command:
            handler(browser, lang)
            return

def open_link(browser, lang):
    speak("حسنًا، ما هو الرابط الذي تريد فتحه؟", lang=lang)
    link_url = listen(language=lang)
    if link_url:
        browser.get(link_url)
        speak(f"فُتِحَ الرابط: {link_url}", lang=lang)
        # Add custom logic for reading content if needed
    else:
        speak("لم يتم اكتشاف تعليمات صوتية. حاول مرة أخرى.", lang=lang)

def fill_form(browser, lang):
    speak("جارٍ قراءة الحقول في الاستمارة.", lang=lang)

    input_elements = browser.find_elements_by_tag_name('input')

    if not input_elements:
        speak("عذرًا، لا توجد حقول في هذه الصفحة.", lang=lang)
        return

    speak("الحقول المتاحة:")

    field_names = [element.get_attribute('name') for element in input_elements]
    for field_name in field_names:
        speak(field_name, lang=lang)

    speak("أي حقل تود ملؤه؟", lang=lang)
    chosen_field = listen(language=lang)

    if chosen_field and chosen_field in field_names:
        speak(f"حسنًا، يرجى ملء حقل {chosen_field}.", lang=lang)
        user_input = listen(language=lang)
        if user_input:
            browser.find_element_by_name(chosen_field).send_keys(user_input)
            speak(f"تم ملء حقل {chosen_field} بنجاح.", lang=lang)
        else:
            speak("عذرًا، لم يتم اكتشاف تعليمات صوتية. حاول مرة أخرى.", lang=lang)
    else:
        speak("عذرًا، الحقل الذي اخترته غير متاح أو لم يتم فهمه. حاول مرة أخرى.", lang=lang)

# Add other functions here

# ...

# Check for Ctrl key presses to launch the program
if keyboard.is_pressed('ctrl'):
    launch_program(custom_commands)
