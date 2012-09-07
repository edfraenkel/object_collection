class ObjectCollection(list):
  """
  Bundles objects together in a list and allows to retrieve and filter their attributes in a list.

  An example for ObjectCollection

  >>> class ABC(object):
  ...   def __init__(self, a, b, c):
  ...     self.a = a
  ...     self.b = b
  ...     self.c = c
  ...     
  ...   def __repr__(self):
  ...     return "There %s %s %s %s." % ('is' if self.c < 2 else "are", self.c, self.a, self.b)

  >>> object_list = [
  ...   ABC('good', 'cow',       1), 
  ...   ABC('good', 'cows',      2), 
  ...   ABC('bad',  'cows',      3), 
  ...   ABC('bad',  'cows',      4), 
  ...   ABC('ugly', 'cows',      5), 
  ...   ABC('ugly', 'supercows', 6), 
  ... ]

  >>> oc = ObjectCollection(object_list)
  >>> oc
  [There is 1 good cow., There are 2 good cows., There are 3 bad cows., There are 4 bad cows., There are 5 ugly cows., There are 6 ugly supercows.]
  >>> oc.filter(lambda x: x.a == 'ugly')
  [There are 5 ugly cows., There are 6 ugly supercows.]
  >>> oc.filter(lambda x: 'cows' in x.b).b
  ['cows', 'cows', 'cows', 'cows', 'supercows']
  >>> oc.filter(lambda x: 'cows' in x.b).b.filter(lambda x: 'super' in x)
  ['supercows']
  >>> oc.apply(lambda x: x.c**2)
  [1, 4, 9, 16, 25, 36]
  >>> oc.d
  [False, False, False, False, False, False]
  >>> oc = ObjectCollection()
  >>> oc
  []
  >>> oc.append('cheeze')
  >>> oc.append('mozarella')
  >>> oc
  ['cheeze', 'mozarella']
  >>> oc.capitalize()
  ['Cheeze', 'Mozarella']
  """
  def __init__(self, object_list=[]):
    super(ObjectCollection, self).__init__(object_list)
    
  def __getattr__(self, name):
    """Retrieves if the ObjectCollection is a list [a, b, c] this returns [a.name, b.name, c.name]"""
    if name.startswith('__') and name.endswith('__'):
      raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))
    return ObjectCollection([getattr(obj, name, False) for obj in self])
    
  def __call__(self, *args, **kwargs):
    return ObjectCollection([obj(*args, **kwargs) if obj else None for obj in self])

  def filter(self, filter_function):
    """Filters the list in the ObjectCollection with the filter_function"""
    return ObjectCollection([obj for obj in self if filter_function(obj)])
    
  def apply(self, function):
    """Creates a new list with function applied to the elements of the list"""
    return ObjectCollection([function(obj) for obj in self])
  
  @staticmethod
  def __merge_trees(target, other):
    if not other:
      return
    for key, value in other.items():
      if key not in target:
        target[key] = value
      else:
        ObjectCollection.__merge_trees(target[key], value)
  
  def collection_tree(self):
    collection_tree = dict()
    for tree in self.tree():
      ObjectCollection.__merge_trees(collection_tree, tree)
    return collection_tree

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
