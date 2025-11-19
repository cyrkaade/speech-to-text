# Medicament Recognition - Usage Examples

## Quick Start Testing

### Test Phrases in Russian

Try recording these phrases to test medicament recognition:

#### Example 1: Simple Prescription
**Say:** "Назначаю Амоксициллин 500 миллиграмм три раза в день"
**Expected:** Accurate transcription of "Амоксициллин" and dosage instructions

#### Example 2: Multiple Medications
**Say:** "Принимаю Аспирин утром и Омепразол вечером"
**Expected:** Both "Аспирин" and "Омепразол" recognized correctly

#### Example 3: Pharmacy Request
**Say:** "Мне нужен Лазолван сироп или Бромгексин таблетки"
**Expected:** "Лазолван" and "Бромгексин" with correct forms

#### Example 4: Allergy Information
**Say:** "У меня аллергия на Парацетамол и Ибупрофен"
**Expected:** Both medicament names recognized

#### Example 5: Complex Prescription
**Say:** "Метформин 850 миллиграмм два раза в день после еды, и Глюкофаж утром"
**Expected:** "Метформин" and "Глюкофаж" both recognized

### Test Phrases in Kazakh

#### Example 1
**Say:** "Маған Парацетамол және Ибупрофен керек"
**Expected:** Medicament names recognized in Kazakh context

#### Example 2
**Say:** "Күніне үш рет Амоксициллин ішу керек"
**Expected:** "Амоксициллин" recognized with Kazakh instructions

## Testing Steps

1. **Start the Application**
   ```bash
   python app.py
   ```

2. **Open Browser**
   Navigate to: http://localhost:5000

3. **Select Language**
   - Choose "Russian (Русский)" for Russian medicaments
   - Choose "Kazakh (Қазақ)" for Kazakh context
   - Choose "Auto-detect" for mixed language

4. **Record Your Speech**
   - Click "Start Recording"
   - Speak clearly one of the test phrases above
   - Click "Stop Recording"

5. **Verify Results**
   - Check that medicament names are spelled correctly
   - Verify medical terms are recognized
   - Note: The AI response will provide context-aware feedback

## Common Medicaments to Test

### Cardiovascular
- Кардиомагнил, Конкор, Лозап, Эналаприл, Бисопролол

### Pain Relief
- Парацетамол, Ибупрофен, Нурофен, Найз, Кетанов

### Antibiotics
- Амоксициллин, Азитромицин, Сумамед, Амоксиклав

### Digestive
- Омепразол, Мезим, Панкреатин, Эспумизан, Линекс

### Respiratory
- Лазолван, Амброксол, Бромгексин, АЦЦ

## Troubleshooting

### Medicament Not Recognized?

1. **Check Vocabulary**: Verify the medicament is in `medicaments_vocabulary.py`
2. **Adjust Boost**: Increase boost value in the vocabulary file
3. **Pronunciation**: Speak clearly and at moderate speed
4. **Add to Vocabulary**: If missing, add it to MEDICAMENTS_RU or MEDICAMENTS_KK

### Poor Accuracy?

1. **Check Microphone**: Ensure good audio quality
2. **Reduce Background Noise**: Record in quiet environment
3. **Speak Clearly**: Pronounce medicament names distinctly
4. **Select Correct Language**: Match the language selector to your speech

## Advanced Testing

### Testing Custom Vocabulary Addition

1. Edit `medicaments_vocabulary.py`:
   ```python
   MEDICAMENTS_RU = [
       # ... existing ...
       "Ваш Новый Препарат",
   ]
   ```

2. Restart the application:
   ```bash
   # Stop the server (Ctrl+C)
   python app.py
   ```

3. Test the new medicament in your recording

### Testing Different Boost Values

Modify in `app.py`:
```python
speech_context = get_compact_speech_context(
    boost_medicaments=30,  # Try different values (15-40)
    boost_medical_terms=15
)
```

## Validation Checklist

- [ ] Russian medicaments recognized correctly
- [ ] Kazakh medicaments recognized correctly
- [ ] Dosage information captured accurately
- [ ] Medical terms (таблетка, капсула, etc.) transcribed
- [ ] Multi-medicament sentences handled
- [ ] Language selector working properly
- [ ] AI provides relevant medical context

## Performance Metrics

**Expected Accuracy:**
- Medicaments in vocabulary: >95% accuracy
- Medical terms: >90% accuracy
- Overall transcription: >85% accuracy (with good audio)

**Factors Affecting Accuracy:**
- Audio quality
- Background noise
- Pronunciation clarity
- Medicament in vocabulary
- Language consistency

## Support

If you encounter issues:
1. Check console logs for errors
2. Verify SONIOX_API_KEY is set
3. Review medicaments_vocabulary.py for the term
4. Check network connectivity to Soniox API

## Next Steps

After successful testing:
1. Add more medicaments specific to your use case
2. Fine-tune boost values for your needs
3. Integrate with your healthcare workflow
4. Consider adding database tracking for recognized medicaments
