import pymdptoolbox.src.mdptoolbox.example as ex 
import pymdptoolbox.src.mdptoolbox.mdp as mdp

P, R = ex.forest()
vi = mdp.ValueIteration(P, R, 0.96)
print(type(P))
print(P.shape)

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
