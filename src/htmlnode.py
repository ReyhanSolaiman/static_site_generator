class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{str(self.props[prop])}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

        if value is None:
            raise ValueError("LeafNode must have a value")

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return str(self.value)
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
        