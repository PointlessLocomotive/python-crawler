import indicoio
indicoio.config.api_key = '98b26a72259df5f8df1f280747a6f6d6'

text =" ¿Qué hicieron los candidatos al Gobierno del Estado de México para combatir la pobreza? ¡Compara y decide!…"
# single example
x =indicoio.analyze_text(text, apis=['sentiment',  'political', 'keywords','text_tags' ])
print(x)
