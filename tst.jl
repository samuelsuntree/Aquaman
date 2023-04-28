using WaterLily, StaticArrays, PlutoUI, Interpolations, Plots, Images, Statistics
using LinearAlgebra: norm2
using ImageView

_nthread = Threads.nthreads()
if _nthread==1
    @warn "WaterLily.jl is running on a single thread.\n
Launch Julia with multiple threads to enable multithreaded capabilities:\n
    \$julia -t auto $PROGRAM_FILE"
else
    print("WaterLily.jl is running on ", _nthread, " thread(s)\n")
end

function block(L=2^5, radius=20;Re=250,U=0.1,amp=π/4,ϵ=0.5,thk=2ϵ+√2)
    # Line segment SDF
    function sdf(x,t)
        return norm2(x) - radius
    end
    # Oscillating motion and rotation
    function map(x,t)
        α = amp*cos(t*U/L); R = @SMatrix [cos(α) sin(α); -sin(α) cos(α)]
        R * (x.-SVector(3L,4L) + [0.,t/40])
    end
    Simulation((6L+2,6L+2),zeros(2),L;U,ν=U*L/Re,body=AutoBody(sdf,map),ϵ)
end

swimmer = block()
cycle = range(0, 4π, length=24*8)

# plot the vorcity ω=curl(u) scaled by the body length L and flow speed U
function plot_vorticity(sim,t)
	@inside sim.flow.σ[I] = WaterLily.curl(3, I, sim.flow.u) * sim.L / sim.U
	contourf(sim.flow.σ',
			 color=palette(:BuGn), clims=(-10, 10), linewidth=0,
			 aspect_ratio=:equal, legend=true, border=:none)
end


# make a gif over a swimming cycle
@gif for t ∈ sim_time(swimmer) .+ cycle
	sim_step!(swimmer, t, remeasure=true, verbose=false)
	plot_vorticity(swimmer,t)
end

# moyFull = []

# # plot the pressure scaled by the body length L and flow speed U
# function plot_pressure(sim, t)
#     append!(moyFull,[mean(sim.flow.p)]) 
# end


# # make a gif over a swimming cycle
# @gif for t ∈ sim_time(swimmer) .+ cycle
# 	sim_step!(swimmer, t, remeasure=true, verbose=false)
# 	plot_pressure(swimmer, t)
# end

scatter(swimmer.pois.n,
    labels=permutedims(["Number of iteration of the pressure solver"]),
    xlabel="scaled time",
    ylabel="scaled pressure")