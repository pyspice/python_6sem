import sys
import argparse
from itertools import chain
from dialogsgenerator import Agent, RandomDialog

def generate(dialog, count_dialogs=5):
    """
    Генерирует count_dialogs диалогов с помощью rd.generate().
    Возвращаемый объект является генератором.
    """
    b = '_' * 40
    yield from chain(*map(lambda i: chain(iter(['{}Dialog {}{}\n'.format(b, i, b)]), dialog.generate()), range(count_dialogs)))

def write(dialogs, target):
    """
    Записывает сгенерированные диалоги dialogs (это объект-генератор) в поток target.
    """
    for i in dialogs:
        target.write(i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='generates a random dialog')
    
    parser.add_argument('-o', '--output', nargs='?', 
                        const='sys.stdout', default='sys.stdout',
                        help="output stream name, default='sys.stdout'")
    
    parser.add_argument('-t', '--trump_kb', nargs='?', 
                        const='../trump.csv', default='../trump.csv',
                        help="Trump's replicas csv filename, default='../trump.csv'")

    parser.add_argument('-c', '--clinton_kb', nargs='?', 
                        const='../clinton.csv', default='../clinton.csv',
                        help="Clinton's replicas csv filename, default='../clinton.csv'")
    
    parser.add_argument('dialogs_count', type=int,
                        help='total number of dialogs to generate')   
    
    parser.add_argument('max_dialog_len', type=int,
                        help='max length of generated dialogs')       
    
    args = parser.parse_args()
    
    if args.output == 'sys.stdout':
        fout = sys.stdout
    elif args.output == 'sys.stderr':
        fout = sys.stderr
    else:
        fout = open(args.output, 'w', encoding='utf-8')

    dialog = RandomDialog([Agent(args.clinton_kb, "clinton"), Agent(args.trump_kb, "trump")], max_len=args.max_dialog_len)
    
    write(generate(dialog, args.dialogs_count), fout)