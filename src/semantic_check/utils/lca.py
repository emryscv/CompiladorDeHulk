from semantic_check.utils.Type import Type

def get_LCA(type_a: Type, type_b: Type):
    visited = {"*"}
    
    visited.add(type_a.name)    
    
    while type_a.parent:
        type_a = type_a.parent
        visited.add(type_a.name)
        
    while type_b.parent:
        if type_b.name in visited:
            return type_b
        else:
            type_b = type_b.parent
        
    if type_b.name in visited:
        return type_b
    
    return None