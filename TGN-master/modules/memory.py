# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:56:38 2020

@author: Ming Jin
"""

import torch
from torch import nn
from collections import defaultdict


class Memory(nn.Module):
    """
    Memory class, represented as 'S' in the paper

    INIT INPUT:
        n_nodes: Number of unique ndoes
        memory_dimension: Memory dimension
        input_dimension: Message dimension
    """

    def __init__(self, n_nodes, memory_dimension, input_dimension, device="cpu"):

        super(Memory, self).__init__()

        self.n_nodes = n_nodes
        self.memory_dimension = memory_dimension
        self.input_dimension = input_dimension
        # self.message_dimension = message_dimension
        self.device = device

        # self.combination_method = combination_method

        self.__init_memory__()

    def __init_memory__(self):
        """
        Initializes the memory to all zeros.
        It should be called at the start of each epoch.
        """

        # Treat memory as parameter so that it is saved and loaded together with the model
        # requires_grad has been set as FALSE
        self.memory = nn.Parameter(
            torch.zeros((self.n_nodes, self.memory_dimension)).to(self.device),
            requires_grad=False,
        )
        self.last_update = nn.Parameter(
            torch.zeros(self.n_nodes).to(self.device), requires_grad=False
        )

        self.messages = defaultdict(list)

    def store_raw_messages(self, nodes, node_id_to_messages):
        """
        Set nodes' raw message (i.e. self.message) by values in node_id_to_messages
        """
        for node in nodes:
            self.messages[node].extend(node_id_to_messages[node])

    def get_memory(self, node_idxs):
        """
        Return node_idxs' memory
        """
        return self.memory[node_idxs, :]

    def set_memory(self, node_idxs, values):
        """
        Set node_idxs' memory by values
        """
        self.memory[node_idxs, :] = values

    def get_last_update(self, node_idxs):
        """
        Return node_idxs' last updated timestamp
        """
        return self.last_update[node_idxs]

    def backup_memory(self):
        """
        Return a copy of all nodes' memory, last update timestamp, and message
        """
        messages_clone = {}
        for k, v in self.messages.items():
            messages_clone[k] = [(x[0].clone(), x[1].clone()) for x in v]

        return self.memory.data.clone(), self.last_update.data.clone(), messages_clone

    def restore_memory(self, memory_backup):
        """
        Set all nodes' memory, last update timestamp, and message by using memory_backup
        """
        self.memory.data, self.last_update.data = (
            memory_backup[0].clone(),
            memory_backup[1].clone(),
        )

        self.messages = defaultdict(list)
        for k, v in memory_backup[2].items():
            self.messages[k] = [(x[0].clone(), x[1].clone()) for x in v]

    def detach_memory(self):
        """
        Detach memory and all stored messages from the network
        """
        self.memory.detach_()

        # Detach all stored messages
        for k, v in self.messages.items():
            new_node_messages = []
            for message in v:
                new_node_messages.append((message[0].detach(), message[1]))

            self.messages[k] = new_node_messages

    def clear_messages(self, nodes):
        """
        Clear given nodes' message
        """
        for node in nodes:
            self.messages[node] = []
