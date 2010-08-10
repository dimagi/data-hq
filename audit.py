from django.template import VariableNode, Node, TextNode
from django.template.loader import get_template
from django.template.loader_tags import ExtendsNode, BlockNode
from django.template.defaulttags import WithNode


'''
Method loads template and iterates through the template's NodeList to 
check for auditable types. Currently does not consider the request
type.

@param template_name: string name of template to load
@param auditable: list of objects to audit
@return: dictionary of occurrences of object...
for debugging, right now string representation 
'''

def audit(template_name, context, auditable=None):
    # Initialize template and nodes
    template = get_template(template_name)
    nodeList = template.nodelist
    
    temp = []
    result = []
    temp = expandWithNodes(expandBlockNodes(expandExtendNodes(nodeList)))
    
    for node in temp:
        if isinstance(node, VariableNode):
            result.append(node)
    return result

def expandExtendNodes(nodeList):
    result = []
    for node in nodeList:
        if isinstance(node, ExtendsNode):
            result += expandExtendNodes(node.nodelist)
        else:
            result += node
    return result

def expandBlockNodes(nodeList):
    result = []
    for node in nodeList:
        if isinstance(node, BlockNode):
            result += expandBlockNodes(node.nodelist)
        else:
            result += node
    return result 

def expandWithNodes(nodeList):
    result = []
    for node in nodeList:
        if isinstance(node, WithNode):
            result += expandWithNodes(node.nodelist)
        else:
            result += node
    return result 

def expandForNodes(nodeList):
    result = []
    for node in nodeList.nodelist_loop:
        result += node
    return result