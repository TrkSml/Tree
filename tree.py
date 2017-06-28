
import os
from collections import deque
import argparse

class Tree:

	unity_score=5
	unity_space=5

	def __init__(self,PATH):
		self.PATH=PATH
		self.min_sep=PATH.count(os.sep)

	def findall_files_and_directories_size(self,PATH):

		if PATH.endswith('/'):
			PATH=PATH[:-1]
		
		# if  os.path.isfile(PATH):
		# 	return PATH

		total = os.path.getsize(PATH)
		list_size=[total]
		if os.path.isdir(PATH):

			try: 
				for el in os.listdir(PATH):

					childpath = PATH+'/'+el	
					list_size += self.findall_files_and_directories_size(childpath)
						

			except OSError:
				print 'Permission Denied : ',PATH

					#if os.path.isdir(PATH+'/'+el):

		return list_size


	
	def findall_files_and_directories(self,PATH):

		if PATH.endswith('/'):
			PATH=PATH[:-1]
		
		# if  os.path.isfile(PATH):
		# 	return PATH


		list=[]
		if os.path.isdir(PATH):

			try: 
				for el in os.listdir(PATH):
						if os.path.isdir(PATH+'/'+el):
							childpath = PATH+'/'+el	
							list.extend([childpath])
							list.extend(self.findall_files_and_directories(childpath))

						if os.path.isfile(PATH+'/'+el):
						#list.append(PATH)
							list.append(PATH+'/'+el)

			except OSError:
				print 'Permission Denied : ',PATH

					#if os.path.isdir(PATH+'/'+el):

		return list


	def __margin(self,element):
		return element.count(os.sep)-self.min_sep

	def calculate_margins(self,PATH):
		return map(self.__margin,self.findall_files_and_directories(PATH))

	def show_margin_for_each_document_or_folder(self):
		for el in self.findall_files_and_directories(self.PATH):
			print el


	def detect_edges_and_diff_on_the_right(self,list,i):
	

		try :
			while(list[i]==list[i-1] and i<=(len(list)-1)):
				i+=1
		except IndexError:
			pass


		if i>(len(list)-1):
			return list[i-2]-list[i-1]

		return list[i-1]-list[i]
		

	def store_edges(self,PATH):

		result=[]
		margins_calc=self.calculate_margins(PATH)
		for i in range(len(margins_calc)):
			result+=[self.detect_edges_and_diff_on_the_right(margins_calc,i)]

		result=deque(result)
		result.rotate(-1)

		return list(result)


	def store_single_void(self,marg_list,test_item_margin_index,final_item_margin_index,margin,list_of_margins):

		#while list[test_item_margin_index] > list[final_item_margin_index]-margin+count :
		#if  list[test_item_margin_index] > list[final_item_margin_index]-margin+1:
		element=marg_list[test_item_margin_index]-1
		if not (element) in list_of_margins:
			list_of_margins.append(element)

	 
	def store_voids(self,PATH):

		 minimun_edge_void=2
		 margins_calc=self.calculate_margins(PATH)
		 store_edges=self.store_edges(PATH)

		 store_edges=list(store_edges)

		 result=[[] for _ in range(len(margins_calc))]

		 crawler=0

		 while(crawler<len(result)):
		 	crawler+=1

		 	try :

			 	if store_edges[crawler]>1 and store_edges[crawler+1]<=1 :  
			 		controller=store_edges[crawler]
			 		while controller>=2:
				 		crawler_back=crawler 

				 		while((margins_calc[crawler_back]-1)>(margins_calc[crawler]-controller)):

				 			new=margins_calc[crawler]-controller
				 			if not(new in result[crawler_back]) and new>0:
				 				result[crawler_back].append(new)

				 			crawler_back-=1

				 		controller-=1

			except IndexError :
				pass


		 return result


	def print_margin_v2(self,element,element_void,margin,size=None):

		unit_void=' '+' '*self.unity_space
		unit_fill='|'+' '*self.unity_space

		final_unit_top_part = '|'

		final_unit_file='+'+'-'*self.unity_score+element.split(os.sep)[-1]
		final_unit_directory='+'+'-'*self.unity_score+'/'+element.split(os.sep)[-1]

		help_list_to_draw=[[0] for _ in range(margin)]

		for el in element_void :
			help_list_to_draw[el]=[1]


		#print help_list_to_draw
		
		first_to_draw_top=''
		first_to_draw_down=''

		if len(help_list_to_draw)>1:

			for el in help_list_to_draw[:-1]:

				if el==[0]:
					first_to_draw_top+=unit_fill
					first_to_draw_down+=unit_fill
				elif el==[1]:
					first_to_draw_top+=unit_void
					first_to_draw_down+=unit_void


			if os.path.isdir(element):

				first_to_draw_top+=final_unit_top_part
				first_to_draw_down+=final_unit_directory

			else:

				first_to_draw_top+=final_unit_top_part
				first_to_draw_down+=final_unit_file

		else :

			if os.path.isdir(element):

				first_to_draw_top+=final_unit_top_part
				first_to_draw_down+=final_unit_directory

			else:

				first_to_draw_top+=final_unit_top_part
				first_to_draw_down+=final_unit_file

		if size :

			print first_to_draw_top
			print first_to_draw_down+' : '+str(size)+' kB'

		else:

			print first_to_draw_top
			print first_to_draw_down


	def draw_tree(self,PATH,with_size=None):
		list_of_directories_and_files=self.findall_files_and_directories(PATH)
		list_of_sizes=self.findall_files_and_directories_size(PATH)
		#se=self.store_edges(PATH)
		m=self.calculate_margins(PATH)
		voids=self.store_voids(PATH)
		print PATH.split('/')[-1] if not PATH[-1]=='/' else PATH.split('/')[-2]
		for el1,v in zip(list_of_directories_and_files,range(len(voids))):
		
			try:
				if with_size :
					self.print_margin_v2(el1,voids[v],m[v],list_of_sizes[v])
				else :
					self.print_margin_v2(el1,voids[v],m[v])

			except IndexError:
				pass
			

def parse_and_print():

	parser = argparse.ArgumentParser()
	parser.add_argument("PATH", help="display a tree_like structure of subfolders and subfiles",type=str)

	args = parser.parse_args()

	tr=Tree(args.PATH)
	tr.draw_tree(args.PATH,True)


if __name__=='__main__':

	parse_and_print()

# 	print el.count(os.sep)


#print len(findall(PATH))