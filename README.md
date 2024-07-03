###
```bash
pip install git+https://github.com/mosiwon/ovos_stt_plugin-google-cloud-translate.git
```

## Configuration

* in mycroft.conf
```json
{
  "stt": {
    "module": "google_translate_stt",
    "google_translate_stt": {
      "stt_api_key": "YOUR_GOOGLE_API_KEY",
      "translate_api_key": "YOUR_GOOGLE_API_KEY",
      "language": "ko-KR"
    }
  }
}