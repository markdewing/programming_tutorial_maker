
#ifndef MINI_MPI3_HPP
#define MINI_MPI3_HPP

#include <stdexcept>

#include <mpi.h>

class communicator
{
public:
  communicator(MPI_Comm impl) noexcept : impl_(impl) {}

  int rank() const {
    int rank = -1;
    int s = MPI_Comm_rank(impl_, &rank);
    if (s != MPI_SUCCESS) throw std::runtime_error("MPI_Comm_rank failed");
    return rank;
  }

private:
  MPI_Comm impl_;
};



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

  static inline communicator& get_world_instance()
  {
    static communicator instance{MPI_COMM_WORLD};
    return instance;
  }

  communicator world() const {
    communicator ret{get_world_instance()};
    return ret;
  }

};



#endif /* MINI_MPI3_HPP */
