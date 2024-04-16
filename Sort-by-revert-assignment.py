from __future__ import annotations
import random
import time
from typing import Optional

class Reverter:
    """This class represents an array to be sorted. It formally encodes the states of the problem
    """
    def __init__(self,size:int,init=True) -> None:
        """The class only sorts an array containing numbers 1..size. The constructor shuffles the array in order to create an unsorted array.

        Args:
            size (int): the size of the array
            init (bool, optional): if True, the array is initialized with value 1..size, the shuffled, else, the array
            remains empty (it is used to clone the array). Defaults to True.
        """
        if init:
            self.table=list(range(1,size+1))
            random.shuffle(self.table)
            self.hash()
            self.parent=None
            self.g = 0
            self.h = self.heuristic() # or heuristic3()
            self.f = self.g + self.h
        else:
            self.table=[]
            # Initialize g, h and f to None when init is False
            self.g = None
            self.h = None
            self.f = None

    def __str__(self) -> str:
        """returns a string representation of the object Reverter

        Returns:
            str: the string representation
        """
        return str(self.table)

    def hash(self):
        """Compute a hashcode of the array. Since it is not possible to hash a list, this one is first converted to a tuple
        """
        self.__hash__=hash(tuple(self.table))
    
    def __eq__(self, __value: Reverter) -> bool:
        """Tests whether the current object if equals to another object (Reverter). The comparison is made by comparing the hashcodes

        Args:
            __value (Reverter): _description_

        Returns:
            bool: True if self==__value, else it is False
        """
        return self.__hash__==__value.__hash__
    
    
    def is_the_goal(self) -> bool :
        """Tests whether the table is already sorted (so that the search is stopped)

        Returns:
            bool: True if the table is sorted, else it is False.
        """
        for i in range(1,len(self.table)):
            if self.table[i-1]>self.table[i]:return False
        return True

    # def is_the_goal(self) -> bool:
    #     return all(self.table[i] <= self.table[i+1] for i in range(len(self.table)-1))

    def clone(self) -> Reverter:
        """This methods create a copy of the current object

        Returns:
            Reverter: the copy to be created
        """
        res=Reverter(len(self.table),False)
        res.table=[*self.table]
        res.parent=self
        return res
    
    def actions(self) -> list[Reverter]:
        """This class builds a list of possible actions. The returned list contains a set of tables depending of possible reverting of the current table

        Returns:
            list[Reverter]: the list of tables obtained after applying the possible reverting
        """
        res=[]
        sz=len(self.table)-1
        for i in range(sz):
            r=self.clone()
            v=self.table[i:] #  the items from i to the end
            v.reverse()
            r.table=self.table[:i]+v # items from the beginning to, but NOT including, i, + the reverted sub-table
            # Update g, h, and f values
            r.g = self.g + 1
            r.h = r.heuristic()
            r.f = r.g + r.h

            r.hash()
            res.append(r)
        return res

    def actions3(self) -> list[Reverter]:
        """ Uses heuristic3 method

        Returns:
            list[Reverter]: the list of tables obtained after applying the possible reverting
        """
        res=[]
        sz=len(self.table)-1
        for i in range(sz):
            r=self.clone()
            v=self.table[i:] 
            v.reverse()
            r.table=self.table[:i]+v 
            # Update g, h, and f values
            r.g = self.g + 1
            r.h = r.heuristic3() 
            r.f = r.g + r.h

            r.hash()
            res.append(r)
        return res

    def heuristic(self):
        """somme des éléments supérieurs à gauche et des éléments inférieurs à droite"""
        h = 0
        for i in range(len(self.table)):
            left_sum = sum(1 for j in range(i) if self.table[j] > self.table[i])
            right_sum = sum(1 for j in range(i + 1, len(self.table)) if self.table[j] < self.table[i])
            h += left_sum + right_sum
        return h
    def heuristic3(self):
        """calcule la somme des différences absolues entre la position actuelle de chaque élément et sa position cible dans le tableau trié (proposé)"""
        h = sum(abs(self.table[i] - (i + 1)) for i in range(len(self.table)))
        return h
   
    def solveBreadth(self) -> Optional[Reverter]:
        """This method implements breadth first search"""
        # Ensemble OUVERT
        OUVERT = [self]
        # Ensemble FERME
        FERME = []
        while OUVERT:
            # Sélectionner le premier nœud de OUVERT
            current_node = OUVERT.pop(0)           
            # L'enlever de OUVERT et le mettre dans FERME
            FERME.append(current_node)   
            # Si n est un nœud but, alors la recherche termine avec succès
            if current_node.is_the_goal():
                return current_node , OUVERT, FERME           
            # Calculer les successeurs de n
            successors = current_node.actions()           
            for successor in successors:
                # Vérifier si le successeur est déjà dans FERME ni dans OUVERT
                if successor not in OUVERT and successor not in FERME:
                    OUVERT.append(successor)                    
        # Aucune solution trouvée
        return None

    def solveDepth(self) -> Optional[Reverter]:
        """This method implements depth first search"""
        # Ensemble OUVERT
        OUVERT = [self]
        # Ensemble FERME
        FERME = [] 
        while OUVERT:
            # Sélectionner le dernier nœud de OUVERT
            current_node = OUVERT.pop()
            # L'enlever de OUVERT et le mettre dans FERME
            FERME.append(current_node)
            # Si n est un nœud but, alors la recherche termine avec succès
            if current_node.is_the_goal():
                return current_node , OUVERT, FERME            
            # Calculer les successeurs de n
            successors = current_node.actions()
            for successor in successors:
                # Vérifier si le successeur est déjà dans OUVERT ni dans FERME
                if successor not in OUVERT and successor not in FERME:
                    OUVERT.append(successor)                   
        # Aucune solution trouvée
        return None

    def solveRandom(self) -> Optional[Reverter]:
        """This method implements random search"""

        # Ensemble OUVERT
        OUVERT = [self]
        # Ensemble FERME
        FERME = []
        while OUVERT:
            # Sélectionner aléatoirement un nœud de OUVERT
            current_node = random.choice(OUVERT)
            # L'enlever de OUVERT et le mettre dans FERME
            OUVERT.remove(current_node)
            FERME.append(current_node)         
            # Si n est un nœud but, alors la recherche termine avec succès
            if current_node.is_the_goal():
                return current_node , OUVERT, FERME            
            # Calculer les successeurs de n
            successors = current_node.actions()           
            for successor in successors:
                # Vérifier si le successeur est déjà dans OUVERT ni dans FERME
                if successor not in OUVERT and successor not in FERME:
                    OUVERT.append(successor)
                    
        # Aucune solution trouvée
        return None
        
    def solveHeuristic1(self) -> Optional[Reverter]:
        """This method implements heuristic search (heuristic n° 1: g = 0, h : pour chaque élément, calculer la somme du nombre d éléments supérieurs à gauche et le nombre d éléments inférieurs à droite.)"""
        OUVERT = [self]
        FERME = []
        while OUVERT:
            current_node = min(OUVERT, key=lambda x: x.h, default=None)  # Select the node with the lowest h value
            if current_node is None:
                return None  # No solution found
            OUVERT.remove(current_node)
            FERME.append(current_node)
            if current_node.is_the_goal():
                return current_node, OUVERT, FERME
            successors = current_node.actions()
            for successor in successors:
                if successor not in OUVERT and successor not in FERME:
                    OUVERT.append(successor)                   
        return None
    def solveHeuristic2(self) -> Optional[Reverter]:
        """This method implements heuristic search (heuristic n° 2: g = profondeur et h identique au cas précédent.)"""
        OUVERT = [self]
        FERME = []
        while OUVERT:
            current_node = min(OUVERT, key=lambda x: x.f, default=None)  # Select the node with the lowest f value
            if current_node is None:
                return None  # No solution found 
            OUVERT.remove(current_node)
            FERME.append(current_node)
            if current_node.is_the_goal():
                return current_node, OUVERT, FERME
            successors = current_node.actions()
            for successor in successors:
                if successor not in OUVERT and successor not in FERME:
                    OUVERT.append(successor)
        return None

    def solveHeuristic3(self) ->Optional[Reverter]:
        """This method implements heuristic search (proposed heuristic)"""
        self.h = self.heuristic3()
        OUVERT = [self]
        FERME = []

        while OUVERT:
            # Change the initialisation of h in init to heuristic 3
            current_node = min(OUVERT, key=lambda x: x.f, default=None)# Select the node with the lowest f value
            if current_node is None:
                return None  # No solution found  
            OUVERT.remove(current_node)
            FERME.append(current_node)
            if current_node.is_the_goal():
                return current_node, OUVERT, FERME
            successors = current_node.actions3() # Use actions3 to calculate successors [it uses heuristic3()]
            for successor in successors:
                if successor not in OUVERT and successor not in FERME:
                    OUVERT.append(successor)
        return None
       
size=8#8,...,15,...
rev=Reverter(size,True)
print("Tableau initial :", rev)
# print("g = ", rev.g," h = ", rev.h," f = ", rev.f)

# res = rev.actions()

# sz=len(rev.table)-1
# for i in range(sz):
#     print(res[i], res[i].g)

start_time_1 = time.time()*1000
r1 = rev.solveBreadth()
end_time_1 = time.time()*1000

start_time_2 = time.time()*1000
r2 = rev.solveDepth()
end_time_2 = time.time()*1000

start_time_3 = time.time()*1000
r3 = rev.solveRandom()
end_time_3 = time.time()*1000

start_time_4 = time.time()*1000
r4 = rev.solveHeuristic1()
end_time_4 = time.time()*1000

start_time_5 = time.time()*1000
r5 = rev.solveHeuristic2()
end_time_5 = time.time()*1000

start_time_6 = time.time()*1000
r6 = rev.solveHeuristic3()
end_time_6 = time.time()*1000

print("\nResults:")
print("{:<15} {:<30} {:<20} {:<20} {:<20} {:<10} {:<10} {:<10}".format("Method", "Sorted Table", "OUVERT Size", "FERME Size","time (ms)", "g", "h", "f"))
print("-" * 135)
time1 = int(end_time_1 - start_time_1)
print("{:<15} {:<30} {:<20} {:<20} {:<20}".format("Breadth First", str(r1[0]), len(r1[1]), len(r1[2]), time1))
time2 = int(end_time_2 - start_time_2)
print("{:<15} {:<30} {:<20} {:<20} {:<20}".format("Depth First", str(r2[0]), len(r2[1]), len(r2[2]), time2))
time3 = int(end_time_3 - start_time_3)
print("{:<15} {:<30} {:<20} {:<20} {:<20}".format("Random", str(r3[0]), len(r3[1]), len(r3[2]), time3))
time4 = int(end_time_4 - start_time_4)
print("{:<15} {:<30} {:<20} {:<20} {:<20} {:<10} {:<10} {:<10}".format("Heuristic 1", str(r4[0]), len(r4[1]), len(r4[2]),time4, r4[0].g, r4[0].h, r4[0].f))
time5 = int(end_time_5 - start_time_5)
print("{:<15} {:<30} {:<20} {:<20} {:<20} {:<10} {:<10} {:<10}".format("Heuristic 2", str(r5[0]), len(r5[1]), len(r5[2]),time5, r5[0].g, r5[0].h, r5[0].f))
time6 = int(end_time_6 - start_time_6)
print("{:<15} {:<30} {:<20} {:<20} {:<20} {:<10} {:<10} {:<10}".format("Heuristic 3", str(r6[0]), len(r6[1]), len(r6[2]),time6, r6[0].g, r6[0].h, r6[0].f))



# FERME = r6[2]
# print("Contenu de l'ensemble ferme :")
# for state in FERME:
#     print(state)
 
# OUVERT = r6[1]
# print("Contenu de l'ensemble ouvert :")
# for state in OUVERT:
#     print(state)