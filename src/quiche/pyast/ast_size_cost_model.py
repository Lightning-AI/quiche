from typing import Dict, Tuple

from quiche.analysis import CostModel
from quiche.egraph import ENode, EClassID


class ASTSizeCostModel(CostModel):
    """
    Simple cost model for AST nodes, based on "size", i.e., number of children.
    """

    def enode_cost(self, node: ENode) -> int:
        """
        Calculate the cost of a node based solely on its key (not its children)
        """
        return 1

    def enode_cost_rec(
        self, enode: ENode, costs: Dict[EClassID, Tuple[int, ENode]]
    ) -> int:
        """
        Calculate the cost of a node based on its key and its children

        :param enode: the node to calculate the cost of
        :param costs: dictionary containing costs of children
        """
        child_costs = sum(costs[eid.find()][0] for eid in enode.args)
        return self.enode_cost(enode) + child_costs
