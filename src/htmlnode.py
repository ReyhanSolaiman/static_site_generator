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

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return str(self.value)
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

        # if tag is None:
        #     raise ValueError("ParentNode must have tag")
        # if not children:
        #     raise ValueError("ParentNode must have children")


    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        props = self.props_to_html()

        html = f"<{self.tag}{props}>"

        for child in self.children:
            child_html = child.to_html()
            html += child_html

        html += f"</{self.tag}>"

        return html