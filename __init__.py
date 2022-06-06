from otree.api import *
import random

doc = """
Your app description
"""

#game parameters that stay the same for all players
class C(BaseConstants):
    NAME_IN_URL = 'trustbot_diss1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2
    INSTRUCTIONS_TEMPLATE = 'trustbot_diss1/Instructions.html'
    # Initial amount allocated to each player
    ENDOWMENT = cu(10)
    MULTIPLICATION_FACTOR = 3


#parameters that stay the same for all participants in specific round
class Subsession(BaseSubsession):
      pass

## here we define the treaments that need to be randomized in each round for
## each player
def creating_session(subsession):
    for player in subsession.get_players():
        player.citizen_treatment = 'Yes'
        player.class_treatment = random.choice(['$15,000-$29,999/year','$65,0000-$89,999/year'])
        player.age_treatment = random.choice(['26-36'])
        player.race_treatment = random.choice(['White', 'African American or Black', 
                                    'non-White Hispanic/Latino', 'Asian American']) 


#data/parameters that stay the same for all members of
#one group in specific round.

## this is where Player A can choose how much to send to Player B
class Group(BaseGroup):
    
    sent_amount = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        doc="""Amount sent by P1""",
        label="Please enter an amount from 0 to 10 you would like to send Player B:",
    )
    
    sent_back_amount = models.CurrencyField(doc="""Amount sent back by P2""", min=cu(0))


## this is showing the survey each player have to answer. 

#data/parameters that are unique for each player in a specific round. 
class Player(BasePlayer):
    
    citizen_treatment  = models.StringField()
    age_treatment = models.StringField()
    race_treatment = models.StringField()
    class_treatment  = models.StringField()

  ## Survey questions - note models is essentially a database table. And a field
  ## is the column in a table. 
  
    age = models.StringField(
       choices=[
        [1, '18-25'],
        [2, '26-36'],
        [3, '37-47'],
        [4, '48-59'],
        [5, '60 or above']],
        label= "What is your Age?"
)
    citizen = models.StringField(
        choices=[
            [1, 'Yes'],
            [2, 'No']],
        label= "Are you a US citizen?"
)
    race = models.StringField(
       choices=[
        [1, 'African American or Black'],
        [2, 'White'],
        [3, 'non-White Hispanic/Latino'],
        [4, 'Asian American'],
        [5, 'Other']],
    label= "What is Your Ethnic/Racial Background?"
)
    income = models.StringField(
       choices=[
        [1, '$0-$14,999/year'],
        [2, '$15,000-$29,999/year'],
        [3, '$30,000-$44,999/year'],
        [4, '$45,000–$64,999/year'], 
        [5, '$65,000-$89,999/year'],
        [6, '$90,000 or above']],
    label= "What is Your Income"
)
    
# PAGES - this is what the players actually see when playing the game. 

class Survey(Page):
     form_model = 'player'
     form_fields = ['age', 'citizen', 'race','income'] 
        
     @staticmethod
     def is_displayed(player:Player):
        return player.round_number == 1
     
class WaitForSurvey1(Page):
    
    """
    This is just for show, to make it feel more realistic.
    Also, note it's a Page, not a WaitPage.
    Removing this page won't affect functionality.
    """

    @staticmethod
    def get_timeout_seconds(player: Player):
       if player.round_number == 1:
             return random.randint(2, 10) 
       else:
         return random.randint(2, 5) 

class Send1(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

# form_model is the variable and fields is the responses.This is capturing 
# Player As behavior. 

    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

class WaitForBots1(Page):
    """
    This is just for show, to make it feel more realistic.
    Also, note it's a Page, not a WaitPage.
    Removing this page won't affect functionality.
    """
   
    @staticmethod
    def get_timeout_seconds(player: Player):
        if player.round_number == 1:
              return random.randint(2, 3) 
        else:
          return random.randint(2, 5) 
## this is showing the result of the first bot behavior 

class Results1(Page): 
    
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

# this will show the actual values on the page. 
        return dict(A_sent=A_sent,
                    B_sent_back = B_sent_back,
                    A_received = A_received)


page_sequence = [
    Survey,
    WaitForSurvey1,
    Send1,
    WaitForBots1,
    Results1,
    ]