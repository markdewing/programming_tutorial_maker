
#ifndef MINI_MPI3_HPP
#define MINI_MPI3_HPP

#include <stdexcept>

#include <mpi.h>


inline void finalize()
{
  int s = MPI_Finalize();
  if (s != MPI_SUCCESS) throw std::runtime_error("cannot finalize MPI");

}

inline void initialize(){
  int s = MPI_Init(nullptr, nullptr);
  if (s != MPI_SUCCESS) throw std::runtime_error("cannot initialize MPI");
}


class environment
{
public:
  environment() { initialize(); }
  ~environment() { finalize(); }
};



#endif /* MINI_MPI3_HPP */
