# Notes regarding Steiner Triple Systems and implementation

## Overview:

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