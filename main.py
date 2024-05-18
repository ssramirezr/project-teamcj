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

def follow(symbol, grammar):
    pass

def main():

    grammarsToAnalyze = int(input()) # Number of grammars to be analized

    for _ in range(grammarsToAnalyze):

        numNT = int(input()) # Number of NT's
        grammar = {} # Dictionary for the grammar
        NTsymbols = [] # Array for the NT

        for _ in range (numNT):
            rule = str(input()).split() # Input that contains the rule, split() divides it by spaces
            NTsymbol = rule[0] # Here we specify that the first symbol is the NT
            NTsymbols.append(NTsymbol) # Then we add it to the NT's array
            productions = rule[1:] 
            grammar[NTsymbol] = productions # Grammar instantiation 
        
        print("\n")
        
        # Dictionary for the First()
        firstDictionary = {}

        # FIRST(x) for the non-terminals
        for i in range(len(NTsymbols)):
            

            firstOfSymbol = first(NTsymbols[i], grammar)
            # Add the symbol of the First(X) as the key, the content is the set of First(x)
            firstDictionary[NTsymbols[i]] = firstOfSymbol 
            # Print the First() for every NT
            print(f"First({NTsymbols[i]}) = {printFormat(firstOfSymbol)}")

if __name__ == "__main__":
    main()
    