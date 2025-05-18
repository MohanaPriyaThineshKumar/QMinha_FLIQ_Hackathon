#Local Testing Script 

# 1) Describe how your separate .py testing script works.
# Ans.1) The testing script performs two main checks to validate the circuit. First, it verifies the structure and sequence of gates by comparing the user's circuit with a reference (correct) circuit. Then, it runs the circuit on a simulator to ensure that the final qubit consistently collapses to the zero state. The circuit is considered valid only if both conditions are met.

#2) What does the script check?
# Ans.2)  Gate Sequence Check: Uses a helper function circuits_equal_structure() that compares the  gate sequence (name and position of each gate) between the student’s circuit (ckt) and a correct reference circuit.
#         Output State Check: Runs the circuit on a QASM simulator and checks whether the final measurement results are limited to the set, This indicates that the last qubit (Bond’s qubit) collapses correctly to |0⟩ after applying the inverse RY gate, confirming the teleportation worked.

#3) How can the reader use it to verify correctness before running on real hardware?
# Ans.3)Students or developers can run this script locally to: Ensure their circuit logic and gate sequence are correct. Confirm that the quantum teleportation output behaves as expected in an ideal (simulated) environment.
#This avoids wasting valuable time and resources on real quantum hardware runs, which: Often have long queues and are susceptible to noise.


from qiskit_aer import Aer
from qiskit import transpile, QuantumCircuit
from qiskit import QuantumCircuit

def canonical_gate_sequence(circuit: QuantumCircuit):
    sequence = []
    for instr, qargs, cargs in circuit.data:
        gate_name = instr.name
        qubit_indices = [circuit.qubits.index(q) for q in qargs]
        clbit_indices = [circuit.clbits.index(c) for c in cargs]
        sequence.append((gate_name, tuple(qubit_indices), tuple(clbit_indices)))
    return sequence

def circuits_equal_structure(circ1, circ2):
    return canonical_gate_sequence(circ1) == canonical_gate_sequence(circ2)

def test_add():
    circ = QuantumCircuit(3, 3)
    circ.ry(2*theta, 0)
    circ.h(1)
    circ.cx(1,2)
    circ.barrier()
    circ.cx(0,1)
    circ.h(0)
    circ.barrier()
    circ.measure([0, 1], [0, 1])
    circ.cx(1, 2)
    circ.cz(0, 2)
    circ.ry(2*theta, 2).inverse()
    circ.measure([2], [2])
    #print(circuits_equal_structure(ckt, circ))

    try:
        if(circuits_equal_structure(ckt, circ)):
            simulator = Aer.get_backend("qasm_simulator")
            transpiled_circuit = transpile(ckt, simulator)
            job = simulator.run(transpiled_circuit, shots = 1000)
            result = job.result()
            counts = result.get_counts()
            #print(set(results.get_counts().keys()) == set(['001', '011', '010', '000']))
            if set(results.get_counts().keys()) == set(['001', '011', '010', '000']):
                print("All tests passed!")
        else:
            print("Your circuit is wrong, make sure you are using the correct gates.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_add()
