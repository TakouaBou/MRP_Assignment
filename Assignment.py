from __future__ import annotations
import random
from typing import Optional

class Reverter:
    """This class represents an array to be sorted. It formally encodes the states of the problem
    """
    def __init__(self,size:int,init=True) -> None:
        """The class only sorts an array containing numbers 1..size. The constructor shuffles the array
        in order to create an unsorted array.

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
            self.h = self.heuristic()
            self.f = self.g + self.h
        else:
            self.table=[]

    def __str__(self) -> str:
        """returns a string representation of the object Reverter

        Returns:
            str: the string representation
        """
        return str(self.table)

    def hash(self):
        """Compute a hashcode of the array. Since it is not possible to hash a list, this one is first
        converted to a tuple
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
    
    
    # def is_the_goal(self) -> bool :
    #     """Tests whether the table is already sorted (so that the search is stopped)

    #     Returns:
    #         bool: True if the table is sorted, else it is False.
    #     """
    #     for i in range(1,len(self.table)):
    #         if self.table[i-1]>self.table[i]:return False
    #     return True
    def is_the_goal(self) -> bool:
        return all(self.table[i] <= self.table[i+1] for i in range(len(self.table)-1))

    
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
        """This class builds a list of possible actions. The returned list contains a set of tables depending of possible
        reverting of the current table

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
        OPEN = [self]
        # Ensemble FERME
        CLOSED = []
        while OPEN:
            # Sélectionner le premier nœud de OUVERT
            current_node = OPEN.pop(0)
            
            # L'enlever de OUVERT et le mettre dans FERME
            CLOSED.append(current_node)
            
            # Si n est un nœud but, alors la recherche termine avec succès
            if current_node.is_the_goal():
                return current_node , OPEN, CLOSED
            
            # Calculer les successeurs de n
            successors = current_node.actions()
            
            for successor in successors:
                # Vérifier si le successeur est déjà dans FERME ni dans OUVERT
                if successor not in OPEN and successor not in CLOSED:
                    OPEN.append(successor)
                    
        # Aucune solution trouvée
        return None

    def solveDepth(self) -> Optional[Reverter]:
        """This method implements depth first search"""
        # Ensemble OUVERT
        OPEN = [self]

        # Ensemble FERME
        CLOSED = [] 

        while OPEN:
            # Sélectionner le dernier nœud de OUVERT
            current_node = OPEN.pop()
            # L'enlever de OUVERT et le mettre dans FERME
            CLOSED.append(current_node)

            # Si n est un nœud but, alors la recherche termine avec succès
            if current_node.is_the_goal():
                return current_node , OPEN, CLOSED
            
            # Calculer les successeurs de n
            successors = current_node.actions()
            for successor in successors:
                # Vérifier si le successeur est déjà dans OUVERT ni dans FERME
                if successor not in OPEN and successor not in CLOSED:
                    OPEN.append(successor)
                    
        # Aucune solution trouvée
        return None

    def solveRandom(self) -> Optional[Reverter]:
        """This method implements random search"""

        # Ensemble OUVERT
        OPEN = [self]
        # Ensemble FERME
        CLOSED = []
        while OPEN:
            # Sélectionner aléatoirement un nœud de OUVERT
            current_node = random.choice(OPEN)
            # L'enlever de OUVERT et le mettre dans FERME
            OPEN.remove(current_node)
            CLOSED.append(current_node)
            
            # Si n est un nœud but, alors la recherche termine avec succès
            if current_node.is_the_goal():
                return current_node , OPEN, CLOSED
            
            # Calculer les successeurs de n
            successors = current_node.actions()
            
            for successor in successors:
                # Vérifier si le successeur est déjà dans FERME
                if successor not in OPEN and successor not in CLOSED:
                    OPEN.append(successor)
                    
        # Aucune solution trouvée
        return None
        
    def solveHeuristic1(self) -> Optional[Reverter]:
        """This method implements heuristic search (heuristic n° 1: g = 0, h : pour chaque élément, calculer la somme du nombre d éléments supérieurs à gauche et le nombre d éléments inférieurs à droite.)"""
        OPEN = [self]
        CLOSED = []
        while OPEN:
            current_node = min(OPEN, key=lambda x: x.f, default=None)  # Select the node with the lowest f value
            if current_node is None:
                return None  # No solution found
            OPEN.remove(current_node)
            CLOSED.append(current_node)
            if current_node.is_the_goal():
                return current_node, OPEN, CLOSED
            successors = current_node.actions()
            for successor in successors:
                if successor not in OPEN and successor not in CLOSED:
                    OPEN.append(successor)
                    # Update the g, h, and f values for the successor 
                    successor.g = 0
                    successor.h = successor.heuristic()
                    successor.f = successor.g + successor.h
        return None
    def solveHeuristic2(self) -> Optional[Reverter]:
        """This method implements heuristic search (heuristic n° 2: g = profondeur et h identique au cas précédent.)"""
        OPEN = [self]
        CLOSED = []
        while OPEN:
            current_node = min(OPEN, key=lambda x: x.f, default=None)  # Select the node with the lowest f value
            if current_node is None:
                return None  # No solution found 
            OPEN.remove(current_node)
            CLOSED.append(current_node)
            if current_node.is_the_goal():
                return current_node, OPEN, CLOSED
            successors = current_node.actions()
            for successor in successors:
                if successor not in OPEN and successor not in CLOSED:
                    OPEN.append(successor)
                    # Update the g, h, and f values for the successor
                    successor.g = current_node.g + 1  # Incrementing the depth by 1
                    successor.h = successor.heuristic()  # Computing the heuristic value for the successor
                    successor.f = successor.g + successor.h  # Updating the total cost
        return None

    def solveHeuristic3(self) -> Optional[Reverter]:
        """This method implements heuristic search (proposed heuristic)"""
        OPEN = [self]
        CLOSED = []
        while OPEN:
            current_node = min(OPEN, key=lambda x: x.f, default=None)# Select the node with the lowest f value
            if current_node is None:
                return None  # No solution found  
            OPEN.remove(current_node)
            CLOSED.append(current_node)
            if current_node.is_the_goal():
                return current_node, OPEN, CLOSED
            successors = current_node.actions()
            for successor in successors:
                if successor not in OPEN and successor not in CLOSED:
                    OPEN.append(successor)
                    # Update the g, h, and f values for the successor
                    successor.g = current_node.g + 1  # Incrementing the depth by 1
                    successor.h = successor.heuristic3()  # Compute the heuristic value using the proposed heuristic
                    successor.f = successor.g + successor.h
        return None
       
size=5#8,...,15,...
rev=Reverter(size,True)
print("Tableau initial :", rev)
# res = rev.actions()

# sz=len(rev.table)-1
# for i in range(sz):
#     print(res[i])

r1 = rev.solveBreadth()
r2 = rev.solveDepth()
r3 = rev.solveRandom()
r4 = rev.solveHeuristic1()
r5 = rev.solveHeuristic2()
r6 = rev.solveHeuristic3()

print("\nResults:")
print("{:<15} {:<25} {:<25} {:<25}".format("Method", "Sorted Table", "Open Set Size", "Closed Set Size"))
print("-" * 90)
print("{:<15} {:<25} {:<25} {:<25}".format("Breadth First", str(r1[0]), len(r1[1]), len(r1[2])))
print("{:<15} {:<25} {:<25} {:<25}".format("Depth First", str(r2[0]), len(r2[1]), len(r2[2])))
print("{:<15} {:<25} {:<25} {:<25}".format("Random", str(r3[0]), len(r3[1]), len(r3[2])))
print("{:<15} {:<25} {:<25} {:<25}".format("Heuristic 1", str(r4[0]), len(r4[1]), len(r4[2])))
print("{:<15} {:<25} {:<25} {:<25}".format("Heuristic 2", str(r5[0]), len(r5[1]), len(r5[2])))
print("{:<15} {:<25} {:<25} {:<25}".format("Heuristic 3", str(r6[0]), len(r6[1]), len(r6[2])))



# CLOSED = r6[2]
# print("Contenu de l'ensemble ferme :")
# for step in CLOSED:
#     print(step)
 
# OPEN = r6[1]
# print("Contenu de l'ensemble ouvert :")
# for item in OPEN:
#     print(item)