# Medicament Recognition Feature

## Overview

This speech-to-text application now includes specialized recognition for **Kazakh and Russian medicament names** using Soniox API's custom vocabulary feature (`speech_context`).

## Features

### Language Support
- **Russian (Русский)**: Full support for Russian pharmaceutical terminology
- **Kazakh (Қазақ)**: Support for Kazakh medicament names and medical terms
- **Auto-detect**: Automatic language detection for mixed-language conversations

### Custom Vocabulary
The system includes over 150+ medicament names and medical terms commonly used in Kazakhstan and Russia, including:

#### Categories Covered
1. **Cardiovascular medications**: Аспирин, Кардиомагнил, Конкор, Лозап, Эналаприл, etc.
2. **Antibiotics**: Амоксициллин, Азитромицин, Цефтриаксон, Сумамед, etc.
3. **Analgesics & NSAIDs**: Ибупрофен, Парацетамол, Нимесулид, Диклофенак, etc.
4. **Diabetes medications**: Метформин, Глюкофаж, Сиофор, Инсулин, etc.
5. **Gastrointestinal**: Омепразол, Мезим, Панкреатин, Линекс, etc.
6. **Respiratory**: Амброксол, Бромгексин, АЦЦ, Лазолван, etc.
7. **Antihistamines**: Супрастин, Цетиризин, Лоратадин, Зодак, etc.
8. **Neurological**: Глицин, Фенибут, Пирацетам, Ноотропил, etc.
9. **Vitamins & supplements**: Омега-3, Кальций Д3, Магний Б6, etc.

### Medical Terms Recognition
The system also recognizes common medical terms and phrases:
- Dosage forms: таблетка, капсула, сироп, мазь, инъекция
- Measurements: миллиграмм, грамм, доза
- Instructions: утром, вечером, до еды, после еды, три раза в день

## How It Works

### Technical Implementation

1. **Custom Vocabulary Loading**: The `medicaments_vocabulary.py` module contains comprehensive lists of medicaments in Russian and Kazakh.

2. **Speech Context Configuration**: The Soniox API is configured with custom `speech_context` that boosts recognition of medicament names:
   ```python
   speech_context = {
       "entries": [
           {
               "phrases": ["Амоксициллин", "Парацетамол", ...],
               "boost": 20  # Higher boost for medicaments
           },
           {
               "phrases": ["таблетка", "капсула", ...],
               "boost": 15  # Moderate boost for medical terms
           }
       ]
   }
   ```

3. **Boost Values**:
   - Medicament names: **boost = 20** (high priority)
   - Medical terms: **boost = 15** (moderate priority)
   - Range: -50 to 50 (values outside this range are clipped)

### API Configuration

The transcription function now accepts a `language` parameter:

```python
def transcribe_with_soniox(audio_path: str, language: str = "ru") -> str:
    # Automatically includes medicament vocabulary
    speech_context = get_compact_speech_context(
        boost_medicaments=20,
        boost_medical_terms=15
    )

    config = {
        "api_key": SONIOX_API_KEY,
        "model": "stt-rt-v3",
        "audio_format": "auto",
        "speech_context": speech_context,
        "language": language  # "ru", "kk", or omit for auto-detect
    }
```

## Usage

### Frontend Interface

1. **Select Language**: Choose from the dropdown:
   - Russian (Русский)
   - Kazakh (Қазақ)
   - Auto-detect

2. **Record Audio**: Click the "Start Recording" button and speak your medical consultation or prescription

3. **View Transcript**: The system will accurately transcribe medicament names and medical terms

### Example Use Cases

#### Prescription Documentation
```
User speaks: "Принимайте Амоксициллин 500 миллиграмм три раза в день после еды"
Transcript: "Принимайте Амоксициллин 500 миллиграмм три раза в день после еды"
```

#### Medical Consultation
```
User speaks: "У меня аллергия на Парацетамол и Аспирин"
Transcript: "У меня аллергия на Парацетамол и Аспирин"
```

#### Pharmacy Inquiry
```
User speaks: "Мне нужен Лазолван сироп или АЦЦ таблетки от кашля"
Transcript: "Мне нужен Лазолван сироп или АЦЦ таблетки от кашля"
```

## Customization

### Adding New Medicaments

To add more medicaments to the vocabulary, edit `medicaments_vocabulary.py`:

```python
MEDICAMENTS_RU = [
    # ... existing medicaments ...
    "Новый Препарат",  # Add your medicament here
]

MEDICAMENTS_KK = [
    # ... existing medicaments ...
    "Жаңа Дәрі",  # Add Kazakh medicament here
]
```

### Adjusting Boost Values

You can fine-tune recognition accuracy by adjusting boost values in `app.py`:

```python
speech_context = get_compact_speech_context(
    boost_medicaments=20,  # Increase for higher priority (max 50)
    boost_medical_terms=15  # Adjust as needed
)
```

**Recommended boost values:**
- Start with 15-20 for important terms
- Increase up to 30-40 if terms are not being recognized
- Avoid extreme values (>40 or <-40) as they may reduce overall accuracy

## Performance Considerations

- **API Pricing**: Custom vocabulary uses Soniox's advanced features, which may affect pricing based on token usage
- **Vocabulary Size**: Current implementation includes ~150+ terms, which is efficient for real-time transcription
- **Compact Format**: The system uses grouped phrases in `speech_context.entries` for optimal API performance

## Supported Languages

According to Soniox documentation:
- ✅ Russian (ru) - Fully supported with custom vocabulary
- ✅ Kazakh (kk) - Fully supported with custom vocabulary
- ✅ 60+ other languages available for auto-detection

## Benefits

1. **Medical Accuracy**: Specialized recognition of pharmaceutical names reduces transcription errors
2. **Multilingual Support**: Seamless switching between Russian and Kazakh
3. **Domain-Specific**: Optimized for healthcare and pharmacy use cases
4. **Extensible**: Easy to add new medicaments and medical terms
5. **Real-time**: Fast transcription with custom vocabulary applied automatically

## Limitations

- Custom vocabulary is most effective for the included medicaments
- Very rare or newly released medications may not be in the vocabulary list
- Complex chemical names may require manual addition to the vocabulary
- Boost values need occasional tuning for optimal accuracy

## Future Enhancements

Potential improvements:
- [ ] Database table to track which medicaments are mentioned in transcripts
- [ ] AI-powered medication interaction checking
- [ ] Integration with pharmaceutical databases
- [ ] Pronunciation variants for brand names
- [ ] Medical dosage extraction and validation
- [ ] Multi-language mixing (code-switching) support

## References

- [Soniox API Documentation](https://soniox.com/docs)
- [Soniox Custom Vocabulary Guide](https://soniox.com/docs/speech-recognition/how-to-guides/customization/)
- [Russian Language Support](https://soniox.com/speech-to-text/russian)
- [Kazakh Language Support](https://soniox.com/speech-to-text/kazakh)
