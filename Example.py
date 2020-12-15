from CH import CH

# Instantiate class
ch = CH()

# Edit informations
ch.gold = '1.0e99999'
ch.rubies = 999
ch.autoClickers = 100
ch.decoded['total5MinuteQuests'] = 5500
ch.decoded['account']['name'] = 'Henrique Amaral'

# Generate save file text
print(ch.encode())