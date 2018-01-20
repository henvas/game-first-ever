from random import randint
import time
import sys
import math

def isDead(arr):
    count = -1
    for i in arr:
        count += 1
        if i.hp <= 0:
            i.hp = 0
            arr.pop(count)
            print(i.name, "is dead!")
            return 1
    return 0


def armorAfterPen(attacker,victim):
    victim.armor -= attacker.armorpen
    return victim.armor


# Armor exp function, used in attack() PLS FIX
def damageReduction(attacker, victim):
    armorAfterPen(attacker,victim)
    if victim.armor < 0:
        victim.armor = 0
    # f(x) = percent damage reduction
    fx = 1 - (15 * math.log(1.5 * victim.armor + 1) + 0.1 * victim.armor) / 100
    return fx

def magicReduction(attacker, victim):
    # g(x) = percent magic reduction
    gx = 1 - (15 * math.log(1.5 * victim.mr + 1) + 0.1 * victim.mr) / 100
    return gx

def createSuperHero(hero_array):
    while(1):
        x = input("Do you want to add another superhero?(y/n)")
        if x == "y":
            name = input("Your hero's regular name:")
            hero_name = input("Your hero's hero name:")
            h = input("Your hero's health:")
            a = input("Your hero's attack damage:")
            ar = input("Your hero's armor:")
            ap = input("Your hero's armorpen:")
            man = input("Your hero's mana:")
            mres = input("Your hero's magic resist:")
            print("Abilities: ")
            print("     0: No ability")
            print("     1: Slice N dice(physical)")
            print("     2: Fireball(magic/DoT)")
            print("     3: Earthquake(magic/stun)")
            ab = input("Choose your ability:")
            try:
                health = int(h)
                ad = int(a)
                armor = int(ar)
                armorpen = int(ap)
                mana = int(man)
                mr = int(mres)
                ability = int(ab)
                m = SuperHero(name, hero_name, health, ad, armor, armorpen,mana,mr,ability)
                hero_array.append(m)
                print("\n")
                return 1
            except ValueError:
                print("Wrong input... ")
        elif x == "n":
            print("\n")
            return 0
        else:
            print("Either y or n")



def selectHero(hero_array,names):
    for v in hero_array:
        if v.name.lower() == names.lower():
            return v

def isDoT(hero_array):
    for v in hero_array:
        if v.debuff > 0 and v.debuff < 4:
            return 1
    return 0

def DoT(hero_array):
    for v in hero_array:
        if v.debuff > 0 and v.debuff < 5:
            v.debuff += 1
            v.hp -= 33 * magicReduction(v, v)
            if v.debuff == 5:
                print(v.name, "is burning for ", int(33 * magicReduction(v, v)), "damage")
            else:
                print(v.name, "is burning for ", int(33 * magicReduction(v, v)), "damage for", 5 - v.debuff,
                      "more turn(s)")
        elif v.debuff == 5:
            v.debuff = 0


def isStun(victim):
    if victim.timer > 0 and victim.timer <= 2:
        victim.timer += 1
        victim.stun = 0
        return 0
    if victim.timer > 2:
        victim.timer = 0
    if victim.stun == 1:
        victim.timer = 1
        victim.stun += 1
        return 1
    elif victim.stun > 1:
        victim.stun = 0
        return 0
    else:
        return 0


## function increasing damage of wade for each attack


class Item(object):
    def __init__(self,name,hp,ad,armor,armorpen,mana,mr):
        self.name = name
        self.hp = hp
        self.ad = ad
        self.armor = armor
        self.armorpen = armorpen
        self.mana = mana
        self.mr = mr


class Person(object):
    def __init__(self,name,hp,ad,armor,armorpen,mana,mr,ability):
        self.name = name
        self.hp = hp
        self.ad = ad
        self.armor = armor
        self.armorpen = armorpen
        self.mana = mana
        self.mr = mr
        self.debuff = 0
        self.stun = 0
        self.ability = ability
        self.timer = 0
        self.item = {}

    def reveal_identity(self):
        print("\n")
        print("My name is {}". format(self.name))

    def attack(self,Person):
        if self.name == Person.name:
            return 0
        prev = Person.hp
        Person.hp -= self.ad*damageReduction(self,Person)
        print("\n")
        print("He hit for ~", int(int(prev-Person.hp)),"damage")



class SuperHero(Person):
    def __init__(self,name,hero_name,hp,ad,armor,armorpen,mana,mr,ability):
        super(SuperHero,self).__init__(name,hp,ad,armor,armorpen,mana,mr,ability)
        self.hero_name = hero_name

    def reveal_identity(self):
        super(SuperHero,self).reveal_identity()
        print("... And I am {}".format(self.hero_name))

    def attack(self,Person):
        if self.name == Person.name:
            return 0
        if self.crit():
            prev = Person.hp
            Person.hp -= 1.5*self.ad*damageReduction(self,Person)
            print("\n")
            print("It's a crit!")
            print("He hit for ~",int(prev-Person.hp),"damage")
            return 1
        else:
            super(SuperHero, self).attack(Person)
            return 1

    def crit(self):
        if randint(0, 3) == 0: return 1
        else: return 0

    def sliceNdice(self,Person):
        manacost = 5
        if self.mana < manacost:
            return 2
        if self.name == Person.name:
            return 3
        if self.crit():
            prev = Person.hp
            Person.hp -= 1.5*(60*damageReduction(self,Person) + self.ad*damageReduction(self,Person))
            print("\n")
            print("Slice N Dice")
            print("It's a crit!")
            print("He hit for ~",int(prev-Person.hp),"damage")
            self.mana -= manacost
            return 1
        else:
            prev = Person.hp
            Person.hp -= (60 * damageReduction(self, Person) + self.ad * damageReduction(self, Person))
            print("\n")
            print("Slice N Dice")
            print("He hit for ~", int(prev-Person.hp), "damage")
            self.mana -= manacost
            return 1

    def fireBall(self,Person):
        manacost = 5
        if self.mana < manacost:
            return 2
        if self.name == Person.name:
            return 3
        prev = Person.hp
        Person.hp -= 300 * magicReduction(self, Person)
        Person.debuff = 1
        print("\n")
        print("Fireball!")
        print("He hit for ~", int(prev-Person.hp), "damage")
        self.mana -= manacost
        return 1

    def earthQuake(self,Person):
        manacost = 5
        if self.mana < manacost:
            return 2
        if self.name == Person.name:
            return 3
        prev = Person.hp
        Person.hp -= 50 * magicReduction(self, Person)
        Person.stun = 1
        print("\n")
        print("Earthquake!")
        print("He hit for ~", int(prev-Person.hp), "damage")
        if Person.timer > 0 and Person.timer <= 2:
            print(Person.name, "has recently been stunned, cant be stunned again for",3 - Person.timer, "turns")
        self.mana -= manacost
        return 1

    def add_item(self,item):
        self.item[item.name] = item
        if len(self.item)>0:
            for i in self.item:
                print(i)
                print("dick")
                self.hp += self.item[i].hp
                self.ad += self.item[i].ad
                self.armor += self.item[i].armor
                self.armorpen += self.item[i].armorpen
                self.mana += self.item[i].mana
                self.mr += self.item[i].mr




######### PLAY THE GAME #########

# Initial heroes
# SuperHero(name, hero_name, health, ad, armor, armorpen,mana,mr,ability)
gary = Person('Gary',100,10,0,0,0,0,0)
wade = SuperHero('Wade', 'Deadpool',1000,150,3,10,10,3,1)
bend = SuperHero('Benderdict','Doctor Strange',500,70,10,5,50,5,2)
jon = SuperHero('Jon','Balls',500,100,23,20,20,20,3)
# Initial hero array

print("Bend hp: ", bend.hp)
bend.add_item(Item('sword',500,100,23,20,20,20))
bend.add_item(Item('ting',123,100,23,20,20,20))
print("Bend hp after item: ", bend.hp)
print(bend.item)
array = [gary,wade,bend,jon]



def main():
    while (1):
        if createSuperHero(array) != True:
            break
    nextHero = array[0]
    prevHero = array[len(array)-1]
    count = 0
    print("Players are: ")
    for t in array:
        print(t.name)
    while(1):
        if len(array) < 2:
            print(array[0].name, "wins")
            time.sleep(1)
            sys.exit()
        i = nextHero
        if i == prevHero:
            count += 1
            i = array[count]
        if isDoT(array):
            DoT(array)
        if isStun(i):
            print(i.name, " is stunned")
            count += 1
            if count >= len(array):
                count = 0
            i = array[count]
        while(1):
            print("\n")
            print(i.name,"'s turn!")
            print("Do you want to:")
            print("1. Attack")
            print("2. Reveal identity")
            print("3. Use ability")
            print("4. Exit")
            xstring = input("Enter your choice: ")
            try:
                x = int(xstring)
            except ValueError:
                x = 5
            if x == 1:
                while(1):
                    y = input("Who do you wan't to attack?")
                    target = selectHero(array,y)
                    if target == None:
                        print("Must be one of the heroes")
                    else:
                        if i.attack(target) == 0:
                            print("Can't attack yo own ass")
                        else:
                            if isDead(array):
                                count -= 1
                            break
                break
            if x == 2:
                i.reveal_identity()
                time.sleep(0.5)
                break
            if x == 3:
                while (1):
                    f = input("Who do you wan't to attack?")
                    target = selectHero(array, f)
                    if target == None:
                        print("Must be one of the heroes")
                    else:
                        if i.ability == 0:
                            print("No ability, normal attack instead")
                            while (1):
                                o = input("Who do you wan't to attack?")
                                target = selectHero(array, o)
                                if target == None:
                                    print("Must be one of the heroes")
                                else:
                                    if i.attack(target) == 0:
                                        print("Can't attack yo own ass")
                                    else:
                                        if isDead(array):
                                            count -= 1
                                        break
                            break
                        elif i.ability == 1:
                            AbilityChoice = i.sliceNdice(target)
                            if AbilityChoice == 1:
                                if isDead(array):
                                    count -= 1
                                break
                            elif AbilityChoice == 3:
                                print("Can't attack yo own ass")
                            elif AbilityChoice == 2:
                                print("Not enough mana, normal attack instead")
                                while (1):
                                    o = input("Who do you wan't to attack?")
                                    target = selectHero(array, o)
                                    if target == None:
                                        print("Must be one of the heroes")
                                    else:
                                        if i.attack(target) == 0:
                                            print("Can't attack yo own ass")
                                        else:
                                            if isDead(array):
                                                count -= 1
                                            break
                                break
                        elif i.ability == 2:
                            AbilityChoose = i.fireBall(target)
                            if AbilityChoose == 1:
                                if isDead(array):
                                    count -= 1
                                break
                            elif AbilityChoose == 3:
                                print("Can't attack yo own ass")
                            elif AbilityChoose == 2:
                                print("Not enough mana, attack instead")
                                while (1):
                                    o = input("Who do you wan't to attack?")
                                    target = selectHero(array, o)
                                    if target == None:
                                        print("Must be one of the heroes")
                                    else:
                                        if i.attack(target) == 0:
                                            print("Can't attack yo own ass")
                                        else:
                                            if isDead(array):
                                                count -= 1
                                            break
                                break
                        elif i.ability == 3:
                            AbilityCho = i.earthQuake(target)
                            if AbilityCho == 1:
                                if isDead(array):
                                    count -= 1
                                break
                            elif AbilityCho == 3:
                                print("Can't attack yo own ass")
                            elif AbilityCho == 2:
                                print("Not enough mana, attack instead")
                                while (1):
                                    o = input("Who do you wan't to attack?")
                                    target = selectHero(array, o)
                                    if target == None:
                                        print("Must be one of the heroes")
                                    else:
                                        if i.attack(target) == 0:
                                            print("Can't attack yo own ass")
                                        else:
                                            if isDead(array):
                                                count -= 1
                                            break
                                break

                break
            if x == 4:
                print("Exiting...")
                time.sleep(1)
                sys.exit()
            if x > 4 or x < 1:
                print("Must be either 1,2 or 3")
            else:
                print("You O.K?")
        prevHero = i
        count += 1
        if count >= len(array):
            count = 0
        nextHero = array[count]
        print("\n")
        for j in array:
            print(j.name,"'s health: ", int(j.hp), " --- Mana: ", int(j.mana))
            time.sleep(0.5)
        print("\n")




if __name__ == '__main__':
    main()

