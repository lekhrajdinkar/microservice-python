BOLD='\u001b[1m'
UNDERLINE='\u001b[7m'
REVERSE='\u001b[14m'

RED='\u001b[31m'
GREEN='\u001b[32m'
YELLOW='\u001b[33m'

RESET='\u001b[0m'


def myprint(effect: str, *texts: str) -> None:
    """
    print `text` using ANSI color

    :param texts: sequence of text to be print
    :param effect: color to be applied
    """

    text = ' '.join( text for text in texts)
    output="{}{}{}".format(effect,text,RESET)
    print(output)

def myPrintWithMoreEffect( text: str, *effects: str) -> None:
    """
    print `text` using ANSI color
    :param text: text to be print
    :param effect: sequence of  effects to be applied
    """

    effect = ' '.join( effect for effect in effects)
    output="{}{}{}".format(effect,text,RESET)
    print(output)

def myPrintWithMoreEffect2( *effects: str,  text: str) -> None:
    myPrintWithMoreEffect(text, *effects)


# myprint(RED, "hello Lil liu", "how are you" )
# myprint(GREEN, "hello Lil liu" )
# myprint(BOLD, "hello Lil liu" )
# myprint(UNDERLINE, "hello Lil liu")
