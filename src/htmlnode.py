class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError()

  def props_to_html(self):  
    if self.props is None:
      return ""
    
    result = ""
    for key, value in self.props.items():
      result += f' {key}="{value}"'

    return result

  def __repr__(self):
    return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError('All leaf nodes must have a value')

        if self.tag is None:
            return f'{self.value}'
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
      return f'LeafNode({self.tag}, {self.value}, {self.props})'
                
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('All Parent nodes must have a tag')

        if self.children is None or len(self.children) == 0:
            raise ValueError('All Parent nodes must have children nodes')

        inner_node = ""
        for child_node in self.children:
            inner_node += child_node.to_html()

        return f'<{self.tag}{self.props_to_html()}>{inner_node}</{self.tag}>'
      
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
