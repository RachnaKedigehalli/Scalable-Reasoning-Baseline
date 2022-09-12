mkdir datafiles/$1_instances
python3 instance_generator.py $1 100
echo "Files generated"
python3 reasoning.py $1 &> out.txt
echo "Reasoning done"
grep 'Time taken:' out.txt > results/$1_result.txt
# rm out.txt
