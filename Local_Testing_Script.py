#Local Testing Script 

# 1) Describe how your separate .py testing script works.
# Ans.1)

#2) What does the script check?
# Ans.2) Our testing script checks whether the code runs smoothy throught the qasm simulator and then checks if the final result has all ('001' , '011' , '010', '000').

#3) How can the reader use it to verify correctness before running on real hardware?
# Ans.3) 


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
