import mdptoolbox, mdptoolbox.example
P, R = mdptoolbox.example.forest()
vi = mdptoolbox.mdp.ValueIteration(P, R, 0.96)

vi.verbose

vi.run()
expected = (5.93215488, 9.38815488, 13.38815488)
all(expected[k] - vi.V[k] < 1e-12 for k in range(len(expected)))

print('transicoes')
print(P)
print('recompensa')
print(R)
print('politica')
print(vi.policy)
print('iteracoes?')
print(vi.iter)
