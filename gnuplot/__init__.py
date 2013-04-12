"""`gnuplot`

Tool specific initialization for gnuplot.
"""

#
# Copyright (c) 2013 by Pawel Tomulik
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

__docformat__ = "restructuredText"

import SCons.Builder

class _null : pass

class _GplotRelTo(object):
    """Given a sequence of ``nodes`` return their paths relative to predefined
    ``base``.
    """
    def __init__(self, base):
        """Initializes the functional object
        
        **Arguments**

            - *base* - scons filesystem node representing base file or dir,
        """
        import SCons.Util
        self.base = base

    def __call__(self, nodes, *args, **kw):
        """Given a sequence of ``nodes`` return list of their paths relative to
           ``self.base``."""
        return [ self.base.rel_path(node) for node in nodes ]
   
def _GplotFvars(fdict, base):
    """Prepare command line variables to be passed to gnuplot. The variables
    contain input and output file names to gnuplot script.

    **Arguments**
        
        - *fdict* - file dictionary as returned by ``_gplot_fdict()``,
        - *base* - base node, the returned filenames will be relative to this
          node,

    **Returns**

        a list of ``'name="value"'`` strings.
    """
    import SCons.Util
    
    if not fdict: return []
    return [ "'%s=\"%s\"'" % (k, base.rel_path(v)) for k,v in fdict.items() ]


def _gplot_arg2nodes(env, args, *args2, **kw):
    """Helper function. Convert arguments to a list of nodes.
    
    This function works similarly to ``env.arg2nodes()`` except it handles
    also dictionaries.
    
    **Arguments**

        - *env*   - SCons Environment object,
        - *args*  - arguments representing one or more files,
        - *args2* - other positional arguments (passed to ``env.arg2nodes()``),
        - *kw*    - keyword arguments (passed to ``env.arg2nodes()``).

    **Return**
        
        returns list of nodes.
    """
    import SCons.Util
    if SCons.Util.is_Dict(args):
        return env.arg2nodes(args.values(), *args2, **kw)
    else:
        return env.arg2nodes(args, *args2, **kw)

def _gplot_arg2nodes_dict(env, args, name = None, *args2, **kw):
    """Helper function. Convert arguments to a dict with file nodes.

    **Arguments**

        - *env*  - SCons Environment object,
        - *args* - arguments representing one or more files,
        - *name* - default name used when `args` is not a dictionary,
        - *args2* - other positional arguments (passed to ``env.arg2nodes()``),
        - *kw*    - keyword arguments (passed to ``env.arg2nodes()``).

    **Returns**
        
        dictionary of type ``{ 'key' : node }``,
    """
    import SCons.Util
    if SCons.Util.is_Dict(args):
        keys = args.keys()
        vals = args.values()
        nodes = dict( zip( keys, env.arg2nodes(vals, *args2, **kw) ) )
    elif SCons.Util.is_Sequence(args):
        keys = [ '%s%d' % (name, i+1) for i in xrange(0,len(args)) ]
        nodes = dict( zip( keys, env.arg2nodes(args, *args2, **kw) ) )
    elif args:
        nodes = { '%s%d' % (name,1) : env.arg2nodes(args,*args2,**kw)[0] }
    else:
        nodes = {}

    return nodes


def _gplot_fdict(env):
    """Helper function. Make a dictionary containing gnuplot command-line
    variables with input/output file names.

        Constuction variables ``$gp_inputs``, ``$gp_outputs``,
        and ``$gp_extoutputs`` are processed to create the specific dictionary.
       
        **Arguments**

            - *env* - SCons Environment object,

        **Returns**
            
            returns a ``{ 'name' : 'value' }`` dict where 'name's are
            gnuplot variable names and 'value's are corresponding values,

    """
    def fdict2(env, triples, f = None):
        nodes = {}
        for t in triples:
            try: args = env[t[0]]
            except KeyError: pass
            else:
                name = env.subst('$%s' % t[1])
                if not name: name = t[2]
                nodes.update(_gplot_arg2nodes_dict(env, args, name))

        if f is not None:
            for key, node in nodes.items():
                nodes[key] = f(node)
        return nodes
    result = {}

    triples = [ ('gp_outputs', 'GPLOTOUTVAR', 'output'),
                ('gp_extoutputs', 'GPLOTEOUTVAR', 'eoutput') ]
    result.update(fdict2(env, triples))
    triples = [ ('gp_inputs', 'GPLOTINVAR', 'input') ]
    result.update(fdict2(env, triples, lambda n : n.srcnode() ))
    return result

def _gplot_scan_for_outputs(env, base, source):
    """Helper function. Scan source files for 'set output' gnuplot commands.

    **Arguments**
        
        - *env* - the scons Environment object,
        - *base* - base directory (node) for the file names obtained from source,
        - *source* - list of source nodes to be scanned.

    **Return**
        
        list of output files (as nodes) extracted from the source files
    """
    import re
    _re = r'^\s*set\s+output\s+[\'"]([^\n\r\'"]+)[\'"](?:\s*;\s*)*#?.*$'
    _re = re.compile(_re, re.M)

    nodes = []
    # extract file names
    for src in source:
        contents = src.get_text_contents()
        names = _re.findall(contents)
        # convert to nodes
        nodes.extend(env.File(names, base))
    nodes = list(set(nodes))
    return nodes

def _GplotScanner(node, env, path, arg):
    """Scan gnuplot script for implicit dependencies"""
    deps = []

    # Add input files to implicit dependencies
    try: inputs = env['_gp_input_nodes']
    except KeyError: pass
    else: deps.extend(inputs)

    return deps


def _GplotEmitter(target, source, env):
    """Append gp_outputs and gp_eoutputs to target list. The emitter also
    prepares the list of implicit dependencies for further processing in the
    scanner (see `_GplotScanner()`).
    """
    env['_gp_fdict'] = _gplot_fdict(env)

    try: inputs = env['gp_inputs']
    except KeyError: pass
    else: env['_gp_input_nodes'] = _gplot_arg2nodes(env, inputs)

    outnodes = []
    try: outputs = env['gp_outputs']
    except KeyError: pass
    else: outnodes.extend( _gplot_arg2nodes(env, outputs) )

    try: outputs = env['gp_extoutputs']
    except KeyError: pass
    else: outnodes.extend(_gplot_arg2nodes(env, outputs))

    # env['_gp_output_nodes'] = outnodes

    # scan source files for outpus
    outnodes2 = _gplot_scan_for_outputs(env, env['_gp_chdir'], source)
    for node in outnodes: 
        if node in outnodes2:
            outnodes2.remove(node)
    for node in target: 
        if node in outnodes2:
            outnodes2.remove(node)
    outnodes.extend(outnodes2)

    return  target + outnodes, source 

def GplotGraph(env, target, source=_null, chdir=_null, **kw):
    """The GplotGraph builder (wrapper actually)
    
    **Arguments**
    
        - *env* - the scons Environment object,
        - *target* - (a list of) target node(s) or their names,
        - *source* - (a list of) source node(s) or their names,
        - *chdir* - working directory for gnuplot,
        - *kw* - keywords passed to real builder.
    """
    import SCons.Util

    if target and (source is _null): 
        source = target
        target = []

    ekw = kw.copy()
    if chdir is _null:
        chdir = env.fs.getcwd()
        ekw['_gp_chdir'] = chdir
    elif not chdir:
        # Top source dir
        chdir = SCons.Builder._null
        ekw['_gp_chdir'] = env.Dir('#') 
    else:
        if SCons.Util.is_String(chdir):
            chdir = env.Dir(chdir, env.fs.getcwd())
            ekw['_gp_chdir'] = chdir
        else:
            ekw['_gp_chdir'] = chdir

    return env._GplotGraphBuilder(target, source, chdir, **ekw)

def _detect_gnuplot(env):
    if env.has_key('GNUPLOT'):
        return env['GNUPLOT']
    return env.WhereIs('gnuplot')

def generate(env):
    """Add Builders and construction variables to the Environment"""
    import SCons.Builder, SCons.Script

    gnuplot = _detect_gnuplot(env)
    if not gnuplot: gnuplot = 'gnuplot'
    env['GNUPLOT'] = gnuplot

    fvars   = '$( ${_concat( "%s " % GPLOTVARPREFIX, ' \
            + '_GplotFvars( _gp_fdict, _gp_chdir ), ' \
            + 'GPLOTVARSUFFIX, __env__ )} $)'

    srcs    = '$( ${_concat( "", SOURCES, "", __env__, ' \
            + '_GplotRelTo(_gp_chdir))} $)'

    gnuplotcom  = '$GNUPLOT $GNUPLOTFLAGS %s %s' % (fvars, srcs)
    import SCons.Defaults
    env.SetDefault( GPLOTSUFFIX     = '.gp',
                    GPLOTINVAR      = 'input',
                    GPLOTOUTVAR     = 'output',
                    GPLOTEOUTVAR    = 'eoutput',
                    GPLOTVARPREFIX  = "-e",
                    GPLOTVARSUFFIX  = "",
                    _GplotFvars     = _GplotFvars,
                    _GplotRelTo     = _GplotRelTo,
                    GNUPLOTCOM      = gnuplotcom,
                    GNUPLOTCOMSTR   = '')
    try:
        env['BUILDER']['GplotGraph']
    except KeyError:
        scanner = SCons.Script.Scanner( function = _GplotScanner, argument = None )
        env.Append( BUILDERS = { 
            '_GplotGraphBuilder' :  SCons.Builder.Builder( 
                                action = '$GNUPLOTCOM',
                                src_suffix = '$GPLOTSUFFIX',
                                emitter = _GplotEmitter,
                                source_scanner = scanner
                            ) 
        } )

    try:
        env.AddMethod(GplotGraph, 'GplotGraph')
    except AttributeError:
        # Looks like we use a pre-0.98 version of SCons...
        from SCons.SCript.SConscript import SConsEnvironment
        SConsEnvironment.GplotGraph = GplotGraph

def exists(env):
    return _detect_gnuplot(env)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4 nospell:
