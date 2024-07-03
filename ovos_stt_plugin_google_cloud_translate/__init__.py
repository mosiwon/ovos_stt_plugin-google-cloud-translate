import requests
import json
import base64
from ovos_plugin_manager.templates.stt import STT
from speech_recognition import AudioData
from ovos_utils.log import LOG

class GoogleTranslateSTTPlugin(STT):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stt_api_key = self.config.get("stt_api_key")
        self.translate_api_key = self.config.get("translate_api_key")
        self.language = self.config.get("language", "ko-KR")
        if not self.stt_api_key or not self.translate_api_key:
            raise ValueError("Both STT and Translation API keys are required for Google Translate STT")
        LOG.info(f"GoogleTranslateSTTPlugin initialized with STT API key and Translation API key")

    def execute(self, audio: AudioData, language: str = None) -> str:
        LOG.info("execute called")
        language = language or self.language
        try:
            # Transcribe the audio to text
            transcribed_text = self.transcribe_audio(audio, language)
            LOG.info(f"Transcribed Text: {transcribed_text}")

            # Translate the transcribed text to English
            translated_text = self.translate_text(transcribed_text)
            LOG.info(f"Translated Text: {translated_text}")

            return translated_text
        except Exception as e:
            LOG.error(f"Error in execute: {str(e)}")
            return ""

    def transcribe_audio(self, audio: AudioData, language: str) -> str:
        LOG.info("transcribe_audio called")
        url = f"https://speech.googleapis.com/v1/speech:recognize?key={self.stt_api_key}"

        headers = {
            "Content-Type": "application/json"
        }

        audio_content = base64.b64encode(audio.get_raw_data()).decode("utf-8")

        body = {
            "config": {
                "encoding": "LINEAR16",
                "sampleRateHertz": audio.sample_rate,
                "languageCode": language
            },
            "audio": {
                "content": audio_content
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(body))
        
        if response.status_code != 200:
            LOG.error(f"STT API error: {response.status_code}, {response.text}")
            raise Exception(f"Error: {response.status_code}, {response.text}")

        result = response.json()
        LOG.info("STT successful")

        if 'results' in result and len(result['results']) > 0:
            return result['results'][0]['alternatives'][0]['transcript']
        else:
            LOG.error(f"No transcription results: {result}")
            return ""

    def translate_text(self, text: str, target_language: str = "en") -> str:
        LOG.info("translate_text called")
        url = f"https://translation.googleapis.com/language/translate/v2?key={self.translate_api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }

        body = {
            "q": text,
            "target": target_language,
            "format": "text"
        }

        response = requests.post(url, headers=headers, data=json.dumps(body))
        
        if response.status_code != 200:
            LOG.error(f"Translation API error: {response.status_code}, {response.text}")
            raise Exception(f"Error: {response.status_code}, {response.text}")

        result = response.json()
        LOG.info("Translation successful")
        return result['data']['translations'][0]['translatedText']

    @property
    def available_languages(self):
        return {"ko-KR"}

# 샘플 유효한 구성 설정
GoogleTranslateSTTConfig = {
    lang: [{"lang": lang,
            "display_name": f"GoogleTranslateSTT ({lang})",
            "priority": 70,
            "offline": False}]
    for lang in ["ko-KR"]
}
