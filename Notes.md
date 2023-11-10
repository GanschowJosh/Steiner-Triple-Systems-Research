# Notes regarding Steiner Triple Systems and implementation

## Overview:

A *Steiner triple system* is an ordered pair (S, T) where S is a finite set of *points* or *symbols*, and T is a set of 3-element subsets of S called triples, such that each pair of distinct elements of S occurs together in exactly one triple of T. The *order* of a Steiner triple system (S, T) is the size of the set S, denoted |S|.

- A Steiner system with parameters t, k, n, written S(t, k, n), is an n-element set S together with a set of k-element subsets of S (called **blocks**) with the property that each t-element subset of S is contained in exactly one block
 - The classical definition of Steiner systems also required that k = t + 1. An S(2, 3, n) was (and still is) called a *Steiner triple(or triad) system*.

## *Steiner Triple Systems*

- An S(2, 3, n) is called a **Steiner triple system**, and its blocks are called ***triples***. It is common to see the abbreviation STS(*n*) for a Steiner triple system of order *n*.
- The total number of pairs is *n(n-1)/2*, of which three appear in a triple, and so the total number of triples is *n(n-1)/6*.
 - This shows that *n* must be of the form *6k+1* or *6k+3* for some *k*.
- The projective plane of order 2 (the [fano plane](https://en.wikipedia.org/wiki/Fano_plane)) is an STS(7) and the [affine plane](https://en.wikipedia.org/wiki/Affine_plane_(incidence_geometry)) of order 3 is an STS(9).
- We can degine a multiplication on the set S using the Steiner triple system by setting aa = a for all a in S, and ab = c if {a, b, c} is a triple. 
 - This makes S an idempotent, commutative quasigroup.
    - Idempotent: property of certain operations in mathematics and computer science whereby they can be applied multiple times without changing the result beyond the initial application. Ex: pressing an 'on' button multiple times is an idempotent operation because it has the same effect whether done once or multiple times. Same for an 'off' button.
    - Commutative: changing the order does not change the result.
    - Quasigroup (commutative): a mathematical structure that has a set Q and a binary operation * s.t. for all elements a, b in Q, there is a unique "solution" s in Q that solves the equation s * a = b. The operation * is commutative, which means that the order in which the elements are combined doesn't matter (`a*b = b*a`) 

## Properties

It is clear from the definition of S(t, k, n) that 1 \< *t* \< *k* \< *n*

If S(t, k, n) exists, then taking all blocks containing a specific element and discarding that element gives a *derived system* S(t-1, k-1, n-1). Therefore, the existence of S(t-1, k-1, n-1) is a necessary condition for the existence of S(t, k, n)

The number of t-element subsets in S is nCt while the number of t-element subsets in each block is kCt. Since every t-element subset is contained in exactly one block, we have nCt = b(kCt). Thus:

$b = (nCt)/(kCt) = (n(n-1) ... (n-t+1))/(k(k-1) ... (k-t+1))$

where *b* is the number of blocks. Similar reasoning about t-element subsets containing a particular element gives us $((n-1)C(t-1)) = r((k-1)C(t-1))$, or

$r = ((n-1)C(t-1))/((k-1)C(t-1)) = ((n-t+1) ... (n-2)(n-1))/((k-t+1) ... (k-2)(k-1))$

where *r* is the number of blocks containing any given element. From these definitions follows the equation $bk = rn$. It is a necessary condition for the existence of S(t, k, n) that *b* and *r* are integers. As with any block design, [Fisher's inequality](https://en.wikipedia.org/wiki/Fisher%27s_inequality) $b >= n$ is true in Steiner systems.

# From *The Handbook of Combinatorial Designs*

**Theorem** An STS(*v*) ((*v*, 3, 1) BIBD) exists if and only if *v* ≡ 1,3 (mod 6)

**Remark** There are many different proofs of this theorem. The Reverend Thomas P. Kirkman first proved it in 1847 (six years before Steiner posed the question of their existence); Kirkman's solution is recursive. A proof by direct construction is known as Skolem sequences. An elementary recursive proof employs a *v* → 2*v* + 1 construction and a *v* → 2*v* + 7 construction, along with an STS(3), and STS(9) and an STS(13).

**Theorem** An STS(*v*) whose [automorphism](https://en.wikipedia.org/wiki/Automorphism) group contains a (cyclic) automorphism of order *v* exists if and only if *v* ≡ 1,3 (mod 6) and *v* != 9.

**Theorem** A Kirkman triple system of order *v* exists for all positive integers *v* ≡ 3 (mod 6). 
> If (V, B) is an STS(v), W ⊆ V , D = {B ∈ B : B ⊆ W}, and (W, D) is a Steiner
triple system, then (W, D) is a subsystem of (V, B).

**Theorem** (Doyen-Wilson) if *v*, *w* ≡ 1, 3 (mod 6) and *v* ≥ *w* ≥ 1, then there is a STS(*v*) containing a subsystem of order *w* if and only if *v* = *w* or v ≥ 2*w* + 1.
> A large set of STS(v), v ≡ 1, 3 (mod 6), is a partition of the set of all vC3 3-subsetsof v elements into v − 2 STS(v).

**Theorem** (Lu-Teirlinck) A large set of STS(*v*) exists if and only if *v* ≡ 1,3 (mod 6) and *v* != 7.

# Methods for generating STS(*n*)

## Stinson's Algorithm, as described in *Combinatorial algorithms: generation, enumeration, and search*

- **Lemma**: Let (*V*, *B*) be an STS(*v*). Then every point in *V* occurs in exactly $r = (v-1)/2$ blocks and $|B| = v(v-1)/6$

**Proof** To see that $r = (v-1)/2$, it suffices to observe that a point *x* must occur with each of the other *v* - 1 points in a block, and *x* occurs with two other points in each of the *r* blocks in which it occurs.

Let $b = |B|$. To see that $b = v(v-1)/6$, observe that $3b = rv$, since each block contains three points and each of the *v* points occurs in *r* blocks. The result follows.

Clearly, the numbers *r* and *b* defined above must both be integers if an STS(*v*) is to exist. From this it follows that $v ≡ 1 or 3 (mod 6)$ is a necessary condition for the existence of an STS(*v*). It was in fact proved over 100 years ago that an STS(*v*) exists if and only if $v ≡ 1 or 3 (mod 6)$. Thus the simple necessary condition for existence turns out to be sufficient. The proof of sufficiency is constructive, and leads to an efficient method of constructing (at least) one STS(*v*) of every admissable order *v*.

It is also known that the number of non-isomorphic STS(*v*) on a specified point set *V* grows exponentially quickly. One nice feature about the hill-climbing algorithm we are going to describe is that it is very fast, and it is an effective method of constructing apparently random STS(*v*).

In order to use a hill-climbing approach, we formulate the problem as an optimization problem. We first need a definition. A *partial Steiner triple system* is a set system (*V*, *B*) in which every block has size three, and every pair of points from *V* is contained in at most one block. Such a set system is denoted PSTS(*v*), where $v = |V|$. The *size* of a PSTS(*v*) is the number of blocks it contains. It is easy to see that any PSTS(*v*) has size at most $v(v-1)/6$; and a PSTS(*v*) of size $v(v-1)/6$ is in fact an STS(*v*)

We now present the problem of constructing an STS(*v*) in the form of a combinatorial optimization problem.

**Problem:** Construct Steiner Triple System

**Instance:** 
- *a positive integer* $v ≡ 1 or 3 (mod 6)$;
- *a finite set* *V*, $|V| = v$;

**Find:**
- the maximum value of $|B|$ 
- subject to (*V*, *B*) is a PSTS(*v*)

Given *v* and *V*, we will define our universe, *X*, to consist of all sets of blocks *B* such that (*V*, *B*) is a PSTS(*v*). Therefore, any set $B∈X$ is a feasible solution. An optimal solution is any feasible solution have size $v(v-1)/6$.

Instead of explicitly defining a neighborhood function, we instead proceed directly to the description of the heuristic, SWITCH, to be used in the hill-climbing algorithm. The heuristic SWITCH will transform and PSTS(*v*) into a different PSTS(*v*), such that the size either remains the same or is increased by one. This is done by a randomized search strategy, described below.

Let (*V*, *B*) be any PSTS(*v*). A point $x ∈ V$ is called a *live point* if $r_x < (v-1)/2$ where $r_x$ is the number of blocks in *B* that contain the point *x*. A pair of distinct points, ${x, y}$, is called a *live pair* if there is no block $L ∈ B$ such that ${x, y} ⊆ B$.

Now, if (*V*, *B*) has size less than $v(v-1)/6$, then there must exist a live point, say *x*. If *x* is a live point, then there must exist at least two points $y, z ∈ V (y != z)$, such that the pairs ${x, y}$ and ${x, z}$ are both live pairs. (This is because $r_x ≤ (v-3)/2$, and hence *x* has occurred in a block with at most $v-3$ other points.)

Here is the description of the heuristic SWITCH:

```
global NumBlocks
let x be any live point
let y, z be points such that {x, y} and {x, z} are live pairs
if {y,z} is a live pair:
    B = B U {{x, y, z}}
    NumBlocks += 1
else:
    let {w, y, z} ∈ B be the block containing the pair {y,z}
    B = B U {{x, y, z}} \ {{w, y, z}}
```

The heuristic SWITCH constructs a candidate block, {x, y, z} to the system, increasing the size by one. If only two of the three pairs are live, then we add the new block and remove another block {w, y, z} (the unique block containing the pair {y, z}), so the size stays the same.

Here now is the hill climbing algorithm, which keeps applying the heuristic SWITH until a Steiner triple system is finally constructed. The variable NumBlocks records the size of the PSTS(*v*) during the course of the algorithm. 

```
global NumBlocks
NumBlocks = 0
V = {1, ..., v}
B = NULL
while NumBlocks < v(v-1)/6:
    do SWITCH
output (V, B)
```

There is of course no guarantee that the algorithm will ever terminate. But if the choices made by the heuristic SWITCH are random, it seems in practice that the algorithm always terminates successfully by constructing an STS(*v*), and it usually runs very quickly.

### Implementation Details

When we implement the algorithm, it is advantageous to maintain a table (or array) of all the live points. This table does not need to be ordered. When a point ceases to live, the last point in the table can be moved to occupy its place. If a *dead point* becomes live, it is added to the end of the table. In order ot make these updating operations efficient (and to eliminate the need for linear searches of this table), we also need an indexing array, which keeps track of the position of every element in the first table.

In a similar fashion, we will maintain for each live point *x* a table of all the points *y* such that {x, y} is a live pair. Also, for each such table, we have an indexing array. 

This we will have two arrays of length *v*, which we call *LivePoints* and *IndexLivePoints*, and a variable *NumLivePoints*. We have three further arrays which we call *LivePairs*, *IndexLivePairs* and *NumLivePairs*. Each element of *LivePairs* and *IndexLivePairs* is an array of length *v*.

We need one more array, which we name *Other*. For each pair of distinct points {x, y}, this array keeps track of the "other point" in a block containing *x* and *y*. More formally, for any PSTS(*v*), say (V, B), and for any $x, y ∈ V (x != y)$, we define $Other[x,y] = z$ if and only if ${x, y, z} ∈ B$ (and $Other[x, y]$ is undefined if $x, y$ is a live pair).

With the use of the array *Other*, it is unnecessary to explicitly keep track of the block set B during the course of the algorithm. At the end of the algorithm, is is straighforward to compute B from other. This is done by the procedure ConstructBlocks, as shown below

```
B = []
for x in range(1, v):
    for y in range(x+1, v):
        z = Other[x,y]
        if z > y:
            B = B U {{x, y, z}}
return B
```

An initialization of the arrays is performed at the beginning of the hill-climbing algorithm, as follows:

```
global NumLivePoints
global LivePoints[x], IndexLivePoints[x], x = 1, 2, ldots, v
global NumLivePairs[x], x = 1,2, ..., v
global LivePairs[x, y], Other[x, y], x=1,2,...,v, y=1,2,...,v
NumLivePoints = v
for x in range(1, v):
    LivePoints[x] = x
    IndexLivePoints[x] = x
    NumLivePairs[x] = v - 1
    for y in range(1, v-1):
        LivePairs[x,y] = ((y+x-1)%v)+1
    for y in range(1, v):
        IndexLivePairs[x,y] = (y-x)%v
        Other[x,y] = 0
```

It will be necessary to perform "insert" and "delete" operations on these arrays. Thus we define InsertPair and DeletePair as follows.

InsertPair(x,y)

```
global NumLivePoints
global LivePoints[x], IndexLivePoints[x], x = 1,2,...,v
global NumLivePairs[x], x = 1, 2,...,v
global LivePairs[x,y], x = 1,2,...,v, y = 1,2,...,v
if NumLivePairs[x] == 0:
    NumLivePoints += 1
    LivePoints[NumLivePoints] = x
    IndexLivePoints[x] = NumLivePoints
NumLivePairs[x] = NumLivePairs[x]+1
posn = NumLivePairs[x]
livePairs[x, posn] = y
IndexLivePairs[x,y] = posn
```

DeletePair(x,y)

```
global NumLivePoints
global LivePoints[x], IndexLivePoints[x], x = 1, 2,...,v
global NumLivePairs[x], x = 1,2,...,v
global LivePairs[x,y], x = 1,2,...,v,y=1,2,...,v
posn = IndexLivePairs[x,y]
num = NumLivePairs[x]
z = LivePairs[x, num]
LivePairs[x,posn] = z
IndexLivePairs[x,z] = posn
LivePairs[x,num] = 0
IndexLivePairs[x,y] = 0
NumLivePairs[x] -= 1
if NumLivePairs[x] = 0:
    posn = IndexLivePoints[x]
    z = LivePoints[NumLivePoints]
    LivePoints[posn] = z
    IndexLivePoints[z] = posn
    LivePoints[NumLivePoints] = 0
    NumLivePoints += 1
```

These two procedures are used in two higher-level procedures called AddBlock and ExchangeBlock

AddBlock(x,y,z)

```
external DeletePair()
global Other[x,y], x=1,2,...,v, y=1,2,...,v
Other[x,y] = z
Other[y,x] = z
Other[x,z] = y
Other[z,x] = y
Other[y,z] = x
Other[z,y] = x
DeletePair(x,y)
DeletePair(y,x)
DeletePair(x,z)
DeletePair(z,x)
DeletePair(y,z)
DeletePair(z,y)
```

ExchangeBlock(x, y, z, w)

```
external DeletePair(), InsertPair()
global Other[x,y], x=1,2,...,v,y=1,2,...,v
Other[x,y] = z
Other[y,x] = z
Other[x,z] = y
Other[z,x] = y
Other[y,z] = x
Other[z,y] = x
Other[w,y] = 0
Other[y,w] = 0
Other[w,z] = 0
Other[z,w] = 0
InsertPair(w, y)
InsertPair(y, w)
InsertPair(w, z)
InsertPair(z, w)
DeletePair(x, y)
DeletePair(y, x)
DeletePair(x, z)
DeletePair(z, x)
```

Now, we present a more detailed version of the heuristic SWITCH, in which we include the necessary updating for these arrays. 

RevisedSwitch()

```
external AddBlock(), ExchangeBlock()
global NumLivePoints
global LivePoints[x], NumLivePairs[x], x=1,2,..,v
global LivePairs[x, y], Other[x,y], x=1,2,...,v, y=1,2,...,v
let r be a random integer 1<=r<=NumLivePoints
x = LivePoints[r]
let s, t be random integers 1<= s <= t <= NumLivePairs[x]
y = LivePairs[x,s]
z = LivePairs[x,t]
if Other[y,z] == 0:
    AddBlock(x,y,z)
    NumBlocks += 1
else:
    w = Other[y,z]
    ExchangeBlock(x, y, z, w)
```

Here now is the final version of Stinson's algorithm.

RevisedStinsonsAlgorithm(*v*)

```
external ConstructBlocks(), RevisedSwitch()
global NumBlocksOther[x,y], x=1,2,...,v,y=1,2,...v
NumBlocks = 0
Initialize(v)
while NumBlocks < v(v-1)/6:
    RevisedSwitch()
B = ConstructBlocks(v, Other)
output(V,B)
```