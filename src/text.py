import shared
from shared import from_stroop, NumberUtil
from enum import IntEnum

COMMENT_FOOTER = """\n\n
***\n\n
[*^(MayoCoin)*](https://www.reddit.com/r/MayoCoin/)*^( | )*
[*^(MayoCoin Tipper)*](https://github.com/BananoTime/mayo-reddit-tipbot)*^( | )*
[*^(Opt Out)*](https://reddit.com/message/compose/?to=mayo_tipbot&subject=command&message=opt-out)
"""

HELP = """
Help from MayoCoin Tipper! This bot handles tips via the [MayoCoin](https://www.reddit.com/r/MayoCoin/) currency.
[Visit us on GitHub](https://github.com/BananoTime/mayo-reddit-tipbot) for more information on its use and its status. Be sure to read the 
[Terms of Service](https://github.com/BananoTime/mayo-reddit-tipbot#terms-of-service).\n

If you do not accept the Terms of Service, or do not wish to participate, please respond with the text `opt-out`.\n\n

MayoCoin Tipper works in two ways -- either publicly tip a user on a subreddit, or send a PM to /u/mayo_tipbot with a command below.\n\n
To tip 2 Mayo on a tracked subreddit, add the following to the beginning of end of your comment:\n
    !mayo 2
To tip anywhere on reddit, tag the bot as such (it won't post on these subreddits, but it will PM the users):\n
    /u/mayo_tipbot 2
You can tip any amount above the program minimum of 1 Mayo.\n\n

For PM commands, create a new message with any of the following commands (be sure to remove the quotes, '<'s and '>'s):\n
    'create' - Create an account for yourself
    'send <amount or all> <user/address>' - Send Mayo to a reddit user or an address
    'balance' or 'address' - Retrieve your account balance
    'silence <yes/no>' - (default 'no') Prevents the bot from sending you tip notifications or tagging in posts 
    'history <optional: number of records>' - Retrieves tipbot history
    'subreddit' - Shows the subreddits known to the bot
    'opt-out' - Disables your account
    'opt-in' - Re-enables your account 
    'help' - Get this help message\n
For example, if you wanted to send 25 Mayo to user `mrnosock`, reply:\n
    send 25 mrnosock\n    
If you have any questions or bug fixes, please reach out on the [Mayo subreddit](https://reddit.com/r/MayoCoin).\n
The Mayo tip bot is based on the Ananos tipbot. Check out the [Ananos subreddit](https://www.reddit.com/r/Ananos) as well!"""

WELCOME_CREATE = """
Welcome to MayoCoin Tipper, a Reddit tip bot which allows you to tip and send the [MayoCoin](https://reddit.com/r/MayoCoin) currency to your favorite redditors! 
Your account is **active**.\nDeposit MayoCoin by sending it to the address `%s` using your MayoCoin deposit memo `%s`. By using this service, you agree 
to the [Terms of Service](https://github.com/BananoTime/mayo-reddit-tipbot#terms-of-service).\n\n

If you do not accept the Terms of Service, or do not wish to participate, please respond with the text `opt-out`.\n\n

***\n\n
MayoCoin Tipper can be used in two ways. The most common is to tip other redditors publicly by replying to a comment on a tracked subreddit. 
To tip someone 2 Mayo, reply to their message with:\n\n
```!mayo 2```\n\n
To tip a redditor on any subreddit, tag the bot instead of issuing a command:\n\n
```/u/mayo_tipbot 2```\n\n
***\n\n
There are also PM commands by [messaging](https://reddit.com/message/compose/?to=mayo_tipbot&subject=command&message=type_command_here) /u/mayo_tipbot. Remove any quotes, <'s and >'s.\n\n
```send <amount> <valid_stellar_address>``` Withdraw to a Stellar address (must have a trustline with MayoCoin).\n\n
```send <amount> <redditor username>``` Send MayoCoin to another redditor.\n\n
```balance``` Check your account balance.\n\n
```help``` Receive an in-depth help message.\n\n
"""

WELCOME_TIP = """
Welcome to Stellar MayoCoin Tipper, a reddit tip bot which allows you to tip and send the [MayoCoin](https://reddit.com/r/MayoCoin) Currency to your favorite redditors! 
You have just received a MayoCoin tip in the amount of %s Mayo.\n\n
By using this service, you agree to the [Terms of Service](https://github.com/BananoTime/mayo-reddit-tipbot#terms-of-service).\n\n

If you do not accept the Terms of Service, or do not with to participate, please respond with the text `opt-out`.\n\n
***\n\n
MayoCoin Tipper can be used in two ways. The most common is to tip other redditors publicly by replying to a comment on a tracked subreddit. 
To tip someone 2 MayoCoin, reply to their message with:\n\n
```!mayo 2```\n\n
To tip a redditor on any subreddit, tag the bot instead of issuing a command:\n\n
```/u/mayo_tipbot 2```\n\n
***\n\n
There are also PM commands by [messaging](https://reddit.com/message/compose/?to=mayo_tipbot&subject=command&message=type_command_here) /u/mayo_tipbot. Remove any quotes, <'s and >'s.\n\n
```send <amount> <valid_stellar_address>``` Withdraw your Mayo to your own Stellar address (must have a trustline with MayoCoin).\n\n
```send <amount> <redditor username>``` Send Mayo to another redditor.\n\n
```balance``` Check your account balance.\n\n
```help``` Receive an in-depth help message.\n\n
To deposit MayoCoin in your tip bot account, send some to the tip bot address: `%s`. Be sure to specify your deposit memo `%s`.\n
Do not deposit MayoCoin directly from an exchange. 
"""

NEW_TIP = """
Somebody just tipped you %s Stellar MayoCoin! Your creamy new account balance is:\n\n
**%s Mayo**\n\n
To turn off these notifications, reply with "silence yes".
"""

SUBJECTS = {
    "first_tip": "Mayo Tipper - Congrats on receiving your first Mayo Tip!",
    "new_tip": "Mayo Tipper - You just received a new Mayo tip!",
    "deposit": "Mayo Tipper - Deposit successful",
    "help": "Mayo Tipper - Help",
    "balance": "Mayo Tipper - Account Balance",
    "minimum": "Mayo Tipper - Tip Minimum",
    "create": "Mayo Tipper - Create",
    "send": "Mayo Tipper - Send",
    "history": "Mayo Tipper - History",
    "silence": "Mayo Tipper - Silence",
    "subreddit": "Mayo Tipper - Subreddit",
    "opt-out": "Mayo Tipper - Opt Out",
    "opt-in": "Mayo Tipper - Opt In",
    "success": "Mayo Tipper - Your Tip Was Successful",
    "failure": "Mayo Tipper - You Tip Did Not Go Through",
    "convert": "Mayo Tipper - Your Currency Conversion",
    "stats": "Mayo Tipper - Statistics"
}

MINIMUM = {
    "set_min": "Updating tip minimum to %s",
    "below_program": "Did not update. The amount you specified is below the program minimum of %s Mayo.",
    "parse_error": "I couldn't parse your command. I was expecting 'minimum "
    "<amount>'. Be sure to check your spacing.",
}

NAN = "'%s' didn't look like a number to me. If it is blank, there might be extra spaces in the command."

ACCOUNT_MAKE_ERROR_ERROR = "I've experienced an error creating your account, please check with my owner or try again later."
TIP_CREATE_ACCT_ERROR = "I failed to create an account for your intended recipient, please check with my owner or try again later."

class StatusResponse(IntEnum):
    SENT_TO_EXISTING_USER = 10
    SENT_TO_ADDRESS = 11
    DEPOSIT = 12
    SENT_TO_NEW_USER = 20
    NO_ACCOUNT = 100
    SEND_COMMAND_INCORRECT = 110
    SEND_COMMAND_TOO_MANY_ARGS = 111
    CANNOT_PARSE_AMOUNT = 120
    BELOW_PROGRAM_MINIMUM = 130
    BELOW_SUB_MINIMUM = 150
    INSUFFICIENT_FUNDS = 160
    INVALID_USER_OR_ADDRESS = 170
    USER_OPTED_OUT = 190
    CANNOT_SEND_TO_YOURSELF = 200
    SEND_TO_ADDRESS_FAILED = 210
    NOT_ENOUGH_XLM = 220
    NO_TRUSTLINE = 230

# full responses
SEND_TEXT = {
    StatusResponse.SENT_TO_EXISTING_USER: (
        "Sent ```%s Stellar Mayo``` to /u/%s"
    ),
    StatusResponse.SENT_TO_ADDRESS: (
        "Sent ```%s Stellar Mayo``` to %s"
    ),
    StatusResponse.SENT_TO_NEW_USER: (
        "Creating a new account and "
        "sent ```%s Stellar Mayo``` to /u/%s."
    ),
    StatusResponse.DEPOSIT: (
        "A deposit of ```%s Stellar Mayo``` was sent to you (/u/%s)."
    ),    
    StatusResponse.NO_ACCOUNT: (
        "You don't have an account yet. Please [PM me](https://reddit.com/message/compose/?to=mayo_tipbot&subject=command&message=create) with `create` in the body to "
        "make an account."
    ),
    StatusResponse.SEND_COMMAND_INCORRECT: "You must specify an amount and a user, e.g. `send 1 mrnosock`.",
    StatusResponse.SEND_COMMAND_TOO_MANY_ARGS: "Too many arguments specified.",
    StatusResponse.CANNOT_PARSE_AMOUNT: "I could not read the amount. Is '%s' a number?",
    StatusResponse.BELOW_PROGRAM_MINIMUM: "Program minimum is %s Mayo.",
    StatusResponse.BELOW_SUB_MINIMUM: "Your tip is below the minimum for this sub.",
    StatusResponse.INSUFFICIENT_FUNDS: "You have insufficient funds. Please check your balance.",
    StatusResponse.INVALID_USER_OR_ADDRESS: "'%s' is neither a redditor nor a valid address.",
    StatusResponse.USER_OPTED_OUT: "Sorry, the user has opted-out of using Mayo Tipper.",
    StatusResponse.CANNOT_SEND_TO_YOURSELF: "You cannot send to yourself.",
    StatusResponse.SEND_TO_ADDRESS_FAILED: "The amount could not be sent to the specified address. Make sure you have a trustline with Mayo and enough XLM.",
    StatusResponse.NOT_ENOUGH_XLM: "Sorry, my account doesn't have enough XLM to pay the withdrawal fee at this time. Please consider donating some.",
    StatusResponse.NO_TRUSTLINE: "The account you specified does not have a trustline with MayoCoin. This is required by the Stellar network."
}

OPT_IN = """
Welcome back! You have opted back in. Your account is restored."""

OPT_OUT = """
You have opted-out and I promise not to bother you anymore.\n\n
If this was in error, please respond with the text `opt-in`.
"""

SUBREDDIT = {
    "missing": "Your command seems to be missing something. Make sure it follow the format `subreddit <subreddit> "
    "<command> <option>.`",
    "not_mod": "You are not a moderator of /r/%s.",
    "not_maintainer": "You are not a bot maintainer.",
    "minimum": "Sucessfully set your /r/%s minimum to %s, active immediately.",
    "deactivate": "Within 10 minutes, tipping will be deactivated in your subreddit %s.",
    "activate": "Within 10 minutes, the Mayo Tipper response in your Subreddit will be set to %s.",
    "error": "There was something wrong with your activate or minimum command.",
    "all": "Here is a list of every subreddit and its status:\n\nName, Status, Minimum\n\n",
    "one": "Here are the settings for subreddit /r/%s:\n\nName, Status, Minimum\n\n",
}

SILENCE = {
    "yes_no": "I did not see 'no' or 'yes' after 'silence'. If you did type "
    "that, check your spacing.",
    "no": "Silence set to 'no'. You will receive tip notifications and be "
    "tagged by the bot in replies.",
    "yes": "Silence set to 'yes'. You will no longer receive tip "
    "notifications or be tagged by the bot.",
    "parse_error": "I couldn't parse your command. I was expecting 'silence "
    "<yes/no>'. Be sure to check your spacing.",
}

NOT_OPEN = (
    "You do not currently have an open account. To create one, "
    "respond with the text 'create' in the message body."
)

ALREADY_EXISTS = (
    "It looks like you already have an account. In any case it is now "
    "**active**. "
)

BALANCE = (
    "Your balance is:\n\n"
    "**%s Mayo**\n\n"
    "To deposit MayoCoin in your tip bot account, send some to the tip bot address: `%s`. Be sure to specify your deposit memo `%s`.\n\n"
    "Do not deposit MayoCoin directly from an exchange.\n"
)


def make_response_text(message, response):
    status_num = int(response["status"])
    # otherwise, it will be a full response. Even if hostile/silent (we'll send PMs)
    if status_num < 100:
        return SEND_TEXT[status_num] % (
            NumberUtil.format_float(from_stroop(response["amount"])),
            response["recipient"],
        )
    if status_num == StatusResponse.CANNOT_PARSE_AMOUNT:
        return SEND_TEXT[status_num] % response["amount"]
    elif status_num == StatusResponse.BELOW_PROGRAM_MINIMUM:
        return SEND_TEXT[status_num] % shared.PROGRAM_MINIMUM
    elif status_num == StatusResponse.INVALID_USER_OR_ADDRESS:
        return SEND_TEXT[status_num] % response["recipient"]
    else:
        return SEND_TEXT[status_num]
