import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from fitness_app.models import *


class Command(BaseCommand):
    help = 'Populate hardcoded data to db'

    def handle(self, *args, **options):
        add_users()
        add_goals()
        add_sports()
        add_activities()
        add_foods()
        add_meals()
        add_portions()
        add_todays_meal()
        print('populating has finished')


def add_users():
    for user in [
        User.objects.create_user(username='JanNowak', password='pwrpwr123'),
        User.objects.create_user(username='DominikNowak', password='pwrpwr123'),
    ]:
        user.save()


def add_goals():
    Goals.objects.all().filter(pk=2).update(daily_calories=3000, daily_proteins=150, daily_carbs=330, daily_fats=100)


def add_sports():
    for sport in [
        Sport(name='cycling', calories_per_hour=62),
        Sport(name='running', calories_per_hour=81),
        Sport(name='gym', calories_per_hour=112),
    ]:
        sport.save()


def add_foods():
    for food in [
        Food(name='almonds', calories_per_1kg='5830', carbs_per_1kg='62', fats_per_1kg='520', proteins_per_1kg='195'),
        Food(name='apple', calories_per_1kg='860', carbs_per_1kg='800', fats_per_1kg='20', proteins_per_1kg='40'),
        Food(name='avoados', calories_per_1kg='1880', carbs_per_1kg='15', fats_per_1kg='181', proteins_per_1kg='26'),
        Food(name='bananas', calories_per_1kg='860', carbs_per_1kg='188', fats_per_1kg='2', proteins_per_1kg='12'),
        Food(name='beans', calories_per_1kg='360', carbs_per_1kg='60', fats_per_1kg='3', proteins_per_1kg='25'),
        Food(name='beef', calories_per_1kg='1150', carbs_per_1kg='0', fats_per_1kg='29', proteins_per_1kg='221'),
        Food(name='blackberries', calories_per_1kg='580', carbs_per_1kg='85', fats_per_1kg='10', proteins_per_1kg='12'),
        Food(name='bratwurst', calories_per_1kg='3130', carbs_per_1kg='15', fats_per_1kg='245', proteins_per_1kg='224'),
        Food(name='brazil nuts', calories_per_1kg='6790', carbs_per_1kg='45', fats_per_1kg='670',
             proteins_per_1kg='140'),
        Food(name='brea brown', calories_per_1kg='2560', carbs_per_1kg='456', fats_per_1kg='37', proteins_per_1kg='70'),
        Food(name='bread multi-grain', calories_per_1kg='2620', carbs_per_1kg='450', fats_per_1kg='34',
             proteins_per_1kg='95'),
        Food(name='broccoli', calories_per_1kg='290', carbs_per_1kg='20', fats_per_1kg='2', proteins_per_1kg='33'),
        Food(name='brownie', calories_per_1kg='4840', carbs_per_1kg='575', fats_per_1kg='258', proteins_per_1kg='52'),
        Food(name='bulgur', calories_per_1kg='3750', carbs_per_1kg='800', fats_per_1kg='10', proteins_per_1kg='95'),
        Food(name='butter', calories_per_1kg='7350', carbs_per_1kg='7', fats_per_1kg='825', proteins_per_1kg='7'),
        Food(name='cabage', calories_per_1kg='460', carbs_per_1kg='32', fats_per_1kg='9', proteins_per_1kg='43'),
        Food(name='carp', calories_per_1kg='1150', carbs_per_1kg='0', fats_per_1kg='48', proteins_per_1kg='180'),
        Food(name='carrots raw', calories_per_1kg='330', carbs_per_1kg='52', fats_per_1kg='0', proteins_per_1kg='10'),
        Food(name='cashew nuts', calories_per_1kg='5910', carbs_per_1kg='225', fats_per_1kg='465',
             proteins_per_1kg='185'),
        Food(name='cauliflower', calories_per_1kg='240', carbs_per_1kg='30', fats_per_1kg='0', proteins_per_1kg='20'),
        Food(name='celery raw', calories_per_1kg='170', carbs_per_1kg='35', fats_per_1kg='1', proteins_per_1kg='7'),
        Food(name='cottage cheese', calories_per_1kg='1000', carbs_per_1kg='29', fats_per_1kg='42',
             proteins_per_1kg='128'),
        Food(name='cheese feta', calories_per_1kg='2520', carbs_per_1kg='12', fats_per_1kg='215',
             proteins_per_1kg='142'),
        Food(name='cheese mascarpone', calories_per_1kg='4080', carbs_per_1kg='42', fats_per_1kg='420',
             proteins_per_1kg='50'),
        Food(name='cheese mozarella', calories_per_1kg='2460', carbs_per_1kg='46', fats_per_1kg='165',
             proteins_per_1kg='200'),
        Food(name='cherries', calories_per_1kg='520', carbs_per_1kg='110', fats_per_1kg='0', proteins_per_1kg='10'),
        Food(name='chicken breast', calories_per_1kg='1000', carbs_per_1kg='0', fats_per_1kg='9',
             proteins_per_1kg='228'),
        Food(name='chicken leg', calories_per_1kg='1030', carbs_per_1kg='0', fats_per_1kg='23', proteins_per_1kg='206'),
        Food(name='chorizo sausage', calories_per_1kg='3600', carbs_per_1kg='6', fats_per_1kg='300',
             proteins_per_1kg='230'),
        Food(name='cocoa powder', calories_per_1kg='4050', carbs_per_1kg='108', fats_per_1kg='245',
             proteins_per_1kg='198'),
        Food(name='coconut milk', calories_per_1kg='2080', carbs_per_1kg='30', fats_per_1kg='215',
             proteins_per_1kg='15'),
        Food(name='coconut oil', calories_per_1kg='8780', carbs_per_1kg='0', fats_per_1kg='990', proteins_per_1kg='8'),
        Food(name='cod atlantic', calories_per_1kg='720', carbs_per_1kg='0', fats_per_1kg='7', proteins_per_1kg='164'),
        Food(name='cola', calories_per_1kg='440', carbs_per_1kg='110', fats_per_1kg='0', proteins_per_1kg='0'),
        Food(name='corn raw', calories_per_1kg='3540', carbs_per_1kg='655', fats_per_1kg='38', proteins_per_1kg='92'),
        Food(name='cornflakes', calories_per_1kg='3760', carbs_per_1kg='815', fats_per_1kg='8', proteins_per_1kg='79'),
        Food(name='cousous', calories_per_1kg='3680', carbs_per_1kg='740', fats_per_1kg='10', proteins_per_1kg='125'),
        Food(name='duck', calories_per_1kg='2250', carbs_per_1kg='0', fats_per_1kg='172', proteins_per_1kg='181'),
        Food(name='egg', calories_per_1kg='1390', carbs_per_1kg='0', fats_per_1kg='100', proteins_per_1kg='125'),
        Food(name='figs fresh', calories_per_1kg='640', carbs_per_1kg='130', fats_per_1kg='2', proteins_per_1kg='14'),
        Food(name='goat cheese', calories_per_1kg='2050', carbs_per_1kg='40', fats_per_1kg='215',
             proteins_per_1kg='145'),
        Food(name='grapefruit', calories_per_1kg='450', carbs_per_1kg='95', fats_per_1kg='2', proteins_per_1kg='6'),
        Food(name='grapes', calories_per_1kg='530', carbs_per_1kg='115', fats_per_1kg='1', proteins_per_1kg='9'),
        Food(name='halibut', calories_per_1kg='1050', carbs_per_1kg='0', fats_per_1kg='25', proteins_per_1kg='205'),
        Food(name='ham', calories_per_1kg='1620', carbs_per_1kg='14', fats_per_1kg='96', proteins_per_1kg='177'),
        Food(name='hazelnuts', calories_per_1kg='6670', carbs_per_1kg='106', fats_per_1kg='625',
             proteins_per_1kg='142'),
        Food(name='herring', calories_per_1kg='2160', carbs_per_1kg='5', fats_per_1kg='160', proteins_per_1kg='180'),
        Food(name='honey', calories_per_1kg='3080', carbs_per_1kg='755', fats_per_1kg='0', proteins_per_1kg='4'),
        Food(name='hummus', calories_per_1kg='2420', carbs_per_1kg='105', fats_per_1kg='180', proteins_per_1kg='61'),
        Food(name='kefir', calories_per_1kg='630', carbs_per_1kg='45', fats_per_1kg='35', proteins_per_1kg='33'),
        Food(name='kiwi', calories_per_1kg='480', carbs_per_1kg='103', fats_per_1kg='2', proteins_per_1kg='10'),
        Food(name='linseed', calories_per_1kg='4860', carbs_per_1kg='135', fats_per_1kg='325', proteins_per_1kg='200'),
        Food(name='linseed oil', calories_per_1kg='8820', carbs_per_1kg='0', fats_per_1kg='998', proteins_per_1kg='0'),
        Food(name='liver', calories_per_1kg='1320', carbs_per_1kg='20', fats_per_1kg='39', proteins_per_1kg='210'),
        Food(name='mackerel', calories_per_1kg='3440', carbs_per_1kg='0', fats_per_1kg='307', proteins_per_1kg='180'),
        Food(name='mangos', calories_per_1kg='610', carbs_per_1kg='128', fats_per_1kg='3', proteins_per_1kg='11'),
        Food(name='mayonnaise', calories_per_1kg='7410', carbs_per_1kg='25', fats_per_1kg='820', proteins_per_1kg='17'),
        Food(name='melons', calories_per_1kg='470', carbs_per_1kg='70', fats_per_1kg='3', proteins_per_1kg='9'),
        Food(name='milk', calories_per_1kg='460', carbs_per_1kg='48', fats_per_1kg='15', proteins_per_1kg='34'),
        Food(name='mushrooms', calories_per_1kg='160', carbs_per_1kg='3', fats_per_1kg='0', proteins_per_1kg='27'),
        Food(name='mustard', calories_per_1kg='850', carbs_per_1kg='74', fats_per_1kg='40', proteins_per_1kg='50'),
        Food(name='nectarines', calories_per_1kg='360', carbs_per_1kg='75', fats_per_1kg='0', proteins_per_1kg='10'),
        Food(name='noodles rice', calories_per_1kg='3610', carbs_per_1kg='820', fats_per_1kg='6', proteins_per_1kg='50'),
        Food(name='nougats', calories_per_1kg='3950', carbs_per_1kg='765', fats_per_1kg='90', proteins_per_1kg='10'),
        Food(name='oats', calories_per_1kg='3810', carbs_per_1kg='620', fats_per_1kg='70', proteins_per_1kg='135'),
        Food(name='oil', calories_per_1kg='8830', carbs_per_1kg='0', fats_per_1kg='1000', proteins_per_1kg='0'),
        Food(name='onion', calories_per_1kg='360', carbs_per_1kg='61', fats_per_1kg='2', proteins_per_1kg='12'),
        Food(name='oranges', calories_per_1kg='440', carbs_per_1kg='95', fats_per_1kg='2', proteins_per_1kg='10'),
        Food(name='paprika', calories_per_1kg='3530', carbs_per_1kg='350', fats_per_1kg='127', proteins_per_1kg='150'),
        Food(name='parsley', calories_per_1kg='340', carbs_per_1kg='15', fats_per_1kg='2', proteins_per_1kg='44'),
        Food(name='pasta', calories_per_1kg='3590', carbs_per_1kg='670', fats_per_1kg='30', proteins_per_1kg='135'),
        Food(name='peaches', calories_per_1kg='390', carbs_per_1kg='87', fats_per_1kg='1', proteins_per_1kg='8'),
        Food(name='peanuts', calories_per_1kg='6230', carbs_per_1kg='112', fats_per_1kg='520', proteins_per_1kg='260'),
        Food(name='pears', calories_per_1kg='540', carbs_per_1kg='110', fats_per_1kg='3', proteins_per_1kg='5'),
        Food(name='peas', calories_per_1kg='640', carbs_per_1kg='89', fats_per_1kg='0', proteins_per_1kg='45'),
        Food(name='perch', calories_per_1kg='820', carbs_per_1kg='0', fats_per_1kg='8', proteins_per_1kg='185'),
        Food(name='plums', calories_per_1kg='600', carbs_per_1kg='120', fats_per_1kg='6', proteins_per_1kg='8'),
        Food(name='pork', calories_per_1kg='1190', carbs_per_1kg='1', fats_per_1kg='30', proteins_per_1kg='210'),
        Food(name='potatoes', calories_per_1kg='850', carbs_per_1kg='176', fats_per_1kg='1', proteins_per_1kg='20'),
        Food(name='pumpkin', calories_per_1kg='360', carbs_per_1kg='70', fats_per_1kg='2', proteins_per_1kg='11'),
        Food(name='quark', calories_per_1kg='1000', carbs_per_1kg='30', fats_per_1kg='45', proteins_per_1kg='120'),
        Food(name='rabbit', calories_per_1kg='1330', carbs_per_1kg='0', fats_per_1kg='50', proteins_per_1kg='220'),
        Food(name='radishes', calories_per_1kg='180', carbs_per_1kg='25', fats_per_1kg='2', proteins_per_1kg='10'),
        Food(name='red berries', calories_per_1kg='510', carbs_per_1kg='79', fats_per_1kg='1', proteins_per_1kg='11'),
        Food(name='rice', calories_per_1kg='3540', carbs_per_1kg='780', fats_per_1kg='6', proteins_per_1kg='70'),
        Food(name='salmon', calories_per_1kg='2200', carbs_per_1kg='0', fats_per_1kg='157', proteins_per_1kg='202'),
        Food(name='salami sausage', calories_per_1kg='3750', carbs_per_1kg='1', fats_per_1kg='330',
             proteins_per_1kg='195'),
        Food(name='sesame seeds', calories_per_1kg='5810', carbs_per_1kg='60', fats_per_1kg='535',
             proteins_per_1kg='209'),
        Food(name='shrimp', calories_per_1kg='910', carbs_per_1kg='0', fats_per_1kg='19', proteins_per_1kg='185'),
        Food(name='strawberries', calories_per_1kg='360', carbs_per_1kg='65', fats_per_1kg='4', proteins_per_1kg='8'),
        Food(name='sugar brown', calories_per_1kg='3870', carbs_per_1kg='955', fats_per_1kg='0', proteins_per_1kg='0'),
        Food(name='sunflower oil', calories_per_1kg='8810', carbs_per_1kg='0', fats_per_1kg='998',
             proteins_per_1kg='0'),
        Food(name='sweet potato', calories_per_1kg='960', carbs_per_1kg='210', fats_per_1kg='1', proteins_per_1kg='13'),
        Food(name='tomato ketchup', calories_per_1kg='1190', carbs_per_1kg='285', fats_per_1kg='1',
             proteins_per_1kg='5'),
        Food(name='tomatoes', calories_per_1kg='190', carbs_per_1kg='29', fats_per_1kg='2', proteins_per_1kg='10'),
        Food(name='tortilla wraps', calories_per_1kg='5090', carbs_per_1kg='665', fats_per_1kg='100',
             proteins_per_1kg='71'),
        Food(name='tuna', calories_per_1kg='960', carbs_per_1kg='0', fats_per_1kg='10', proteins_per_1kg='215'),
        Food(name='turkey', calories_per_1kg='1060', carbs_per_1kg='0', fats_per_1kg='30', proteins_per_1kg='218'),
        Food(name='veal', calories_per_1kg='1120', carbs_per_1kg='0', fats_per_1kg='29', proteins_per_1kg='213'),
        Food(name='walnuts', calories_per_1kg='6750', carbs_per_1kg='121', fats_per_1kg='625', proteins_per_1kg='144'),
        Food(name='watermelon', calories_per_1kg='370', carbs_per_1kg='78', fats_per_1kg='2', proteins_per_1kg='6'),
        Food(name='wine', calories_per_1kg='860', carbs_per_1kg='30', fats_per_1kg='0', proteins_per_1kg='2'),
        Food(name='yogurt greek', calories_per_1kg='580', carbs_per_1kg='35', fats_per_1kg='4', proteins_per_1kg='102'),
        Food(name='yogurt no-fat', calories_per_1kg='330', carbs_per_1kg='45', fats_per_1kg='1', proteins_per_1kg='34'),
    ]:
        food.save()


def add_meals():
    for meal in [
        Meal(User=User.objects.get(id=1), date_time='2020-1-19T13:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-19T13:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-19T15:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-19T17:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-19T19:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-19T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-20T13:00:00'),
        Meal(User=User.objects.get(id=3), date_time='2020-1-19T13:00:00'),
        Meal(User=User.objects.get(id=3), date_time='2020-1-19T15:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-20T13:00:00'),

        Meal(User=User.objects.get(id=2), date_time='2020-1-17T13:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-17T15:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-17T17:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-17T19:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-17T21:00:00'),

        Meal(User=User.objects.get(id=2), date_time='2020-1-13T13:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-13T15:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-13T17:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-13T19:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-13T21:00:00'),

        Meal(User=User.objects.get(id=2), date_time='2020-1-31T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-30T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-28T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-26T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-24T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-23T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-22T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-21T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-20T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-18T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-17T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-13T21:00:00'),
        Meal(User=User.objects.get(id=2), date_time='2020-1-11T21:00:00'),
    ]:
        meal.save()


def add_portions():
    for portion in [
        Portion(Meal=Meal.objects.get(id=1), Food=Food.objects.get(name='rice'), weight=100),
        Portion(Meal=Meal.objects.get(id=2), Food=Food.objects.get(name='rice'), weight=50),
        Portion(Meal=Meal.objects.get(id=2), Food=Food.objects.get(name='apple'), weight=120),
        Portion(Meal=Meal.objects.get(id=2), Food=Food.objects.get(name='oranges'), weight=30),
        Portion(Meal=Meal.objects.get(id=2), Food=Food.objects.get(name='chicken breast'), weight=330),
        Portion(Meal=Meal.objects.get(id=3), Food=Food.objects.get(name='rice'), weight=250),
        Portion(Meal=Meal.objects.get(id=3), Food=Food.objects.get(name='chicken breast'), weight=550),
        Portion(Meal=Meal.objects.get(id=4), Food=Food.objects.get(name='rice'), weight=50),
        Portion(Meal=Meal.objects.get(id=5), Food=Food.objects.get(name='rice'), weight=50),
        Portion(Meal=Meal.objects.get(id=6), Food=Food.objects.get(name='rice'), weight=50),
        Portion(Meal=Meal.objects.get(id=7), Food=Food.objects.get(name='rice'), weight=1000),
        Portion(Meal=Meal.objects.get(id=8), Food=Food.objects.get(name='apple'), weight=111),
        Portion(Meal=Meal.objects.get(id=9), Food=Food.objects.get(name='apple'), weight=111),
    ]:
        portion.save()


def add_activities():
    for activity in [
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(name='cycling'), duration=90, date='2020-1-10'),
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(name='running'), duration=45, date='2020-1-10'),
        Activity(User=User.objects.get(id=1), Sport=Sport.objects.get(name='gym'), duration=120, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='running'), duration=90, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='running'), duration=60, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='cycling'), duration=60, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=60, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='running'), duration=60, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='cycling'), duration=60, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=75, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=75, date='2020-1-10'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=75, date='2019-1-31'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=75, date='2020-1-30'),
        Activity(User=User.objects.get(id=2), Sport=Sport.objects.get(name='gym'), duration=75, date='2020-1-30'),
        Activity(User=User.objects.get(id=3), Sport=Sport.objects.get(name='gym'), duration=150, date='2020-1-11'),
    ]:
        activity.save()


def add_todays_meal():
    datetimes = [datetime.datetime.combine(datetime.date.today(), datetime.time()).replace(hour=hour)
                 for hour in [9, 12, 15, 18]]
    meals = [Meal(User=User.objects.get(id=2), date_time=dt) for dt in datetimes]
    for meal in meals:
        meal.save()

    for meal in meals:
        p1 = Portion(Meal=meal, Food=Food.objects.get(name='rice'), weight=100)
        p2 = Portion(Meal=meal, Food=Food.objects.get(name='chicken breast'), weight=150)
        p1.save()
        p2.save()
