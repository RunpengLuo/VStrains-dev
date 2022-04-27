## The project is aiming to construct full-length haplotype from metagenomic environment, using pair-end reads


    """
    --------------------------------------------OVERALL FLOW----------------------------------------
    Input: Graph, contig
    operation:
    -> START
    -> flip graph [DONE]
    Output --> graph_L0.gfa

    -> tip removal based on minimap2 [DONE] only apply if graph is not dag
    Output --> t_graph_L1.gfa

    -> cycle detection and node partition
    Output --> nc_graph_L2p.gfa

    -> node depth rebalance + assign edge flow [DONE] 
    Output --> dt_graph_L2.gfa

    -> removed all the node that less than threshold.
    Output --> sdt_graph_L3.gfa

    -> contig coverage rebalance to minimum edge flow along the contig

    -> split graph branch if supported by contig and cov difference < threshold
    Output --> bsdt_graph_L4.gfa

    -> graph compactification (without the contig involved path)
    Output --> cbsdt_graph_L5.gfa

    -> construct contig clique graph
    Output --> cliq_graph.png

    -> based on the contig clique grah topology, concat the contig via the following priority
    PRIORITY
    HIGH
        --> self-cycle contig if no out-in edges exist
        --> self-cycle contig, with in-out from same alter contig
        --> 
    LOW
    -> END
    ------------------------------------------------------------------------------------------------
    """

# current question: 
1. for cand path, which cov assign to it.
2. re-write the shortest path part, use ps path variation and find the best match.
Step to concat the contig clique graph
1. remove any self-cycle edge with curr contig len < min_len (due to high concat risk)
2. for all remaining self-cycle, concat them first.
3. for any pair of contig (u,v) in E, if abs(cov(u) - cov(v)) < threshold, consider the
   contig pair as confident pair, and do the concatenation and merge to a single node as u||v, and remove all the out edges(u) and in edges(v), transfer the in edges(u) to in edges(u||v) and out edges (v) to out edges(u||v)
4. if the cliq graph is cyclic, for any left up cycles, break the cycle by removing the min dist edge among the cycle, only minimum edges be removed until the clique graph is acyclic
5. gradually concat the contigs until no more concatentation exist:
   1. pick any source contig and store into L1 contigs
   2. pick any reachable contigs from L1 contigs and store into L2 contigs, also
      store the relationship between the L1 vs L2 contigs
   3. concat the contig pair (L1-L2) in order of coverage similarity with ascending order, path in between is found by modified Dijkstra search algorithm.
6. for all contigs, if original contig be used within concatenation step but not used up, remove the original contig to reduce the potential duplication ratio.

Step to extend the contig in both end
1. for all src node from graph, concat with a global src node (similarily for sink node)
2. for each contig, find path between gloabl src to the contig head and contig tail to global sink, with distinct direction, path is found via modified Dijkstra search algorithm. Do the end concatentation if path exist.

Step to perform local search on the cand contigs.
1. TODO

Assumption:

No duplicate edges between two nodes

 question: dp estimation is not accurate (with error up to 1000dp)
graph level:
filename format: graph_L{x}.gfa, with x={0,1,2,3}
level -1 graph: assembly graph directly from SPAdes
pre graph: graph after spin the edges
level 0 graph: full-length spades contig reduced graph
level 1 graph: with concatenated candidate strain be reduced
...


TODO: after delete the concated contig, we need to ensure the existence of the rest of the contigs by aligning the path.

TODO: 
1. best recover the contig, when shared-contig node be deleted from specific node, recover it back with original dp.
2. get all the contig from spades with particular constraint.

TODO: what do we do about a satisfied length contig with nodes less than mincov existence for the contig

# graph_draw(graph, vprops={'text': graph.vp.id}, eprops={'text': graph.ep.flow}, output="graph.pdf", output_size=(2000,2000))

Methods & Procedure

1. First, we assemble the input sequence reads by state-of-art assembly tool SPAdes [2] and result into a low error rate sequence De Bruijn graph, which is a directed variation graph with each node represent a short sequence segment and edge represent the overlap between two adjacent nodes. We choose De Bruijn graph as our assembled graph instead of contig variation graph presented in state-of-art approach is to keep the low information loss from the assembly step, use sequence reads to build graph instead of contigs can minimise the dependence for the assembled contig from assembly tools, which can also help us to tackle the cases when contigs cannot cover the full-length haplotype structure.

2. Then, we simplify the graph by spinning the node orientation from the graph, known the sequence read always come with two orientations, “+” and “-”, actual orientation would only be revealed until the full-length sequence be re-constructed. However, based on the assembly graph, we can always find a specific combination of the nodes’ orientation by performing a `spin` operation, such that only one orientation can be used per node. The spin operation is defined as reverse the edge between two nodes and reverse the node orientation to ensure the overlap correctness. We pick the highest depth node as our source node and perform a breadth-first search, in each search iteration, we use the `spin` operation to correct all the neighbouring nodes for the current node, finally we would achieve the single-orientation graph state.

3. Since the assembly graph provides the estimated node coverage (depth) information based on k-mer coverage. For all node N in the graph, since all the neighbouring nodes are connected to N due to end-to-end overlaps, the sum of node coverage for all in-coming/out-going nodes should equal to the node coverage N for consistency. In this case, we can use the node coverage to estimate the edge flow, which is defined as the spread node coverage along all in/out edges. We design an algorithm to assign the edge flow. We initiate the flow to 0 for all edges. For all node N in the graph, we first assign the edge flow if either the in degree (or out degree) of N equals to 1, since the node coverage can only be spread into a single in-coming (or out-going) edge, the edge flow is assigned with no doubt, we iterative the above step until no more edges can be assigned. Then, for rest of unassigned edges with an edge as a tuple: (u, v), we estimate their flow by finding the average between the remaining flow divided by unassigned number of edges for u and the remaining flow divided by unassigned number of edges for v. The algorithm would best fit into viral-based graph, in which edge cross case is minimised.

4. After that, we can align the assembled contigs to the graph for further simplification. Given estimated contig coverage by SPAdes and based on the estimated edge flow from prior step, we can select and extract the high coverage contig from the graph and reduce the edge flow and node depth by the amount of contig coverage, the resulting graph would indicate the nodes that cannot be covered by contigs but may overlap with the contigs and result into a full-length haplotype.

5. Furthermore, we plan to divide the simplified graph into several sub-graphs, then we find all the candidate sub-haplotype and its corresponding abundance each sub-graphs, for each pair of adjacent sub-graphs, we use another sub-graph to overlap them and enhance the correctness for each pair of sub-haplotypes as a merge step [3]. The divide-conquer approach can result into high quality candidate haplotype compared to novel method’s heuristic approach. The sub-haplotype construction method hasn’t been developed. [FIXME]

alternate plan: 
5. For the reduce graph, we only consider the nodes with coverage over 500 dp, which would eliminate nodes that are errorness. From now, we can assemble the secondary contigs from the reduced graph.
   
6. For all contigs both from SPAdes assembly and secondary elimination step, we can merge the contigs to achieve the threshold length sequence. For the merge step, we can align all the reads to the contig ends, and the insert size, distance between the contigs, pair-end information to merge them.
