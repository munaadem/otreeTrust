from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'trustbot_diss1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 4
    INSTRUCTIONS_TEMPLATE = 'trust/instructions.html'
    # Initial amount allocated to each player
    ENDOWMENT = cu(100)
    MULTIPLICATION_FACTOR = 3


class Subsession(BaseSubsession):
      pass

class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        doc="""Amount sent by P1""",
        label="Please enter an amount from 0 to 100 you would like to send Player B:",
    )
    sent_back_amount = models.CurrencyField(doc="""Amount sent back by P2""", min=cu(0))


class Player(BasePlayer):
    pass

# def set_payoffs(group: Group):
#     p1 = group.get_player_by_id(1)


# PAGES
class Introduction(Page):
    pass


class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

class WaitForBots(Page):
    """
    This is just for show, to make it feel more realistic.
    Also, note it's a Page, not a WaitPage.
    Removing this page won't affect functionality.
    """

    @staticmethod
    def get_timeout_seconds(player: Player):
        import random

        return random.randint(1, 3)


class Results(Page):
    

        
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        A_sent = group.sent_amount
        def bot_behavior(A_sent, proportion_kept=0.5):
            A_kept = C.ENDOWMENT - A_sent
            tripled_amount = A_sent*3
            B_kept = tripled_amount*proportion_kept
            B_sent_back = tripled_amount - B_kept
            return B_kept, B_sent_back
        
        B_kept, B_sent_back = bot_behavior(A_sent)
        A_received = (C.ENDOWMENT - A_sent) + B_sent_back
    
        return dict(A_sent=A_sent,
                    B_sent_back = B_sent_back,
                    A_received = A_received)


page_sequence = [
    Introduction,
    Send,
    WaitForBots,
    Results
]