
#include <mini_mpi3.hpp>
#include <iostream>
#include <vector>

int main()
{
  environment env;
  communicator world = env.world();

  // Broadcast_n with raw C++ array
  double va[3]; 
  if (world.rank() == 0) {va[0] = 1.1;}
  world.broadcast_n(va, 3);
  std::cout << "From rank " << world.rank()  << " va[0] = " << va[0] << std::endl;

  // Broadcast_n with std::vector
  std::vector<double> vv{1.0, 2.0, 3.0};
  if (world.rank() == 0) {vv[0] = 4.0;}
  world.broadcast_n(vv.begin(), vv.size());
  std::cout << "From rank " << world.rank()  << " vv[0] = " << vv[0] << std::endl;
  
  return 0;
}
