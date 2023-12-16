import pyttsx3
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import keyboard

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(language="en-US"):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        if language == "ar-AR":
            speak("في انتظار أمرك.")
        elif language == "fr-FR":
            speak("En attente de votre commande.")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio, language=language)
            return user_input
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            if language == "ar-AR":
                speak("عذرًا، لم أستطع فهم طلبك.")
            elif language == "fr-FR":
                speak("Désolé, je n'ai pas pu comprendre votre demande.")
            return ""

def launch_program(commands):
    browser = webdriver.Chrome()
    speak("Program launched.")

    while True:
        user_command = listen()
        if "إغلاق" in user_command or "fermer" in user_command:
            speak("إغلاق البرنامج.")
            break
        else:
            handle_command(user_command, browser, commands)

    browser.quit()

def handle_command(user_command, browser, commands):
    for command, handler in commands.items():
        if command in user_command:
            handler(browser)
            return

def open_link(browser):
    speak("حسنًا، ما هو الرابط الذي تريد فتحه؟")
    link_url = listen()
    if link_url:
        browser.get(link_url)
        speak(f"فُتِحَ الرابط: {link_url}")
        # Add custom logic for reading content if needed
    else:
        speak("لم يتم اكتشاف تعليمات صوتية. حاول مرة أخرى.")

def fill_form(browser):
    speak("جارٍ قراءة الحقول في الاستمارة.")

    # Get all input elements on the page
    input_elements = browser.find_elements_by_tag_name('input')

    if not input_elements:
        speak("عذرًا، لا توجد حقول في هذه الصفحة.")
        return

    speak("الحقول المتاحة:")

    # Read the names of the input fields
    field_names = [element.get_attribute('name') for element in input_elements]
    for field_name in field_names:
        speak(field_name)

    speak("أي حقل تود ملؤه؟")
    chosen_field = listen()

    if chosen_field and chosen_field in field_names:
        speak(f"حسنًا، يرجى ملء حقل {chosen_field}.")
        user_input = listen()
        if user_input:
            # Fill the chosen field with user input
            browser.find_element_by_name(chosen_field).send_keys(user_input)
            speak(f"تم ملء حقل {chosen_field} بنجاح.")
        else:
            speak("عذرًا، لم يتم اكتشاف تعليمات صوتية. حاول مرة أخرى.")
    else:
        speak("عذرًا، الحقل الذي اخترته غير متاح أو لم يتم فهمه. حاول مرة أخرى.")

# Update custom commands
custom_commands = {
    "فتح رابط": open_link,
    "ملء الاستمارة": fill_form,
    # Add more commands as needed
}

# Check for Ctrl key presses to launch the program
if check_ctrl_key():
    launch_program(custom_commands)


# Define custom commands for different websites
custom_commands = {
    "فتح رابط": open_link,
    "ملء الاستمارة": fill_form,
    # Add more commands as needed
}

# Check for Ctrl key presses to launch the program
if check_ctrl_key():
    launch_program(custom_commands)
