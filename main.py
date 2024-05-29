def printFormat(array):

    string = ", ".join(array)
    return f"{{{string}}}"
 
def first(string, grammar):

    # Array that contains the FIRST() set
    firstStr = []

    # If the string starts with a terminal the first is the same terminal
    if string[0].islower():
        firstStr.append(string[0])
        
    else:
        # Productions of the NT in the grammar
        productionsNT =  grammar[string[0]]
        
        # For every production in the NT
        for production in productionsNT:

            # If the production starts with the same NT we skip it
            if production[0] == string[0]:
                continue

            # For every symbol in the production
            for i in range(len(production)):
                # Do the first
                firstStr.extend(first(production[i], grammar))

                # If the first of the leftmost symbol does not contain 
                # the empty string exit the production
                if "e" not in firstStr:
                  break
                else:
                    # Otherwise, verify if the production is not the direct production 
                    # NT -> z and if we are not in the last symbol, remove "z" and 
                    # continue with the next symbol of the production
                    if i != len(production)-1 and len(production) > 1:
                        firstStr.remove("e")

    # Here we eliminate repeated characters and return the FIRST() set
    First= list(set(firstStr))
    First.sort()
    return First

def follow(symbol, grammar, firstDict, followDict):
    # If the FOLLOW set is already calculated, return it
    if symbol in followDict:
        return followDict[symbol]
    
    # Initialize FOLLOW set for the symbol
    followSet = set()

    # Rule 1: If the symbol is the start symbol, add '$' to the FOLLOW set
    if symbol == 'S':
        followSet.add('$')
    
    # Iterate through all productions to apply other rules
    for nt in grammar:
        for production in grammar[nt]:
            # Find all occurrences of the symbol in the production
            for i in range(len(production)):
                if production[i] == symbol:
                    # Rule 2: A → αBβ
                    if i + 1 < len(production):
                        beta = production[i + 1:]
                        firstOfBeta = set()
                        for b in beta:
                            firstOfBeta.update(first(b, grammar))
                            if "e" not in first(b, grammar):
                                break
                        followSet.update(firstOfBeta - {'e'})
                        # Rule 3: If FIRST(β) contains e
                        if 'e' in firstOfBeta:
                            followSet.update(follow(nt, grammar, firstDict, followDict))
                    else:
                        # Rule 3: A → αB
                        if nt != symbol:  # Avoid immediate left recursion
                            followSet.update(follow(nt, grammar, firstDict, followDict))
    
    # Return the FOLLOW() set
    followDict[symbol] = followSet
    return followSet

def main():

    grammarsToAnalyze = int(input()) # Number of grammars to be analized

    for _ in range(grammarsToAnalyze):
        
        print()
        numNT = int(input()) # Number of NT's
        grammar = {} # Dictionary for the grammar
        NTsymbols = [] # Array for the NT

        for _ in range (numNT):
            rule = str(input()).split() # Input that contains the rule, split() divides it by spaces
            NTsymbol = rule[0] # Here we specify that the first symbol is the NT
            NTsymbols.append(NTsymbol) # Then we add it to the NT's array
            productions = rule[1:] 
            grammar[NTsymbol] = productions # Grammar instantiation 
        
        print()
        
        # Dictionary for the First()
        firstDictionary = {}

        # FIRST(x) for the non-terminals
        for i in range(len(NTsymbols)):
            
            # Call the FIRST() function
            firstOfSymbol = first(NTsymbols[i], grammar)
            # Add the symbol of the First(X) as the key, the content is the set of First(x)
            firstDictionary[NTsymbols[i]] = firstOfSymbol 
            # Print the First() for every NT
            print(f"First({NTsymbols[i]}) = {printFormat(firstOfSymbol)}")

        # Dictionary for the FOLLOW() sets
        followDictionary = {}

        # FOLLOW(x) for the non-terminals
        for nt in NTsymbols:

            # Call the FOLLOW() function
            followOfSymbol = follow(nt, grammar, firstDictionary, followDictionary)
            # Print the FOLLOW() for each non-terminal
            print(f"Follow({nt}) = {printFormat(list(followOfSymbol))}")

if __name__ == "__main__":
    main()
    