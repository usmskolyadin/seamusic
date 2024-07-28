import Link from 'next/link';
import Image from 'next/image';
import { useAppDispatch } from '@/shared/hooks/redux';
import { useRouter } from 'next/router';
import { setSong, playSong } from '@/store/reducers/playerSlice';
import default_picture from '@/shared/assets/default-track-picture.png';
import { DefaultButton } from '@/shared/ui/buttons';
import { BeatService } from '@/services';
import { useState, useEffect } from 'react';
import { SongType } from './type';

export function Song({
	id,
	picture,
	name,
	date,
	author,
	album,
	duration,
	src,
	type,
	isAction,
}: SongType) {
	const [deleteId, setDeleteId] = useState(0);
	const dispatch = useAppDispatch();
	const navigate = useRouter();

	const handleDelete = async (id: number) => {
		try {
			const response = await BeatService.delete(id);
			navigate.push('/profile');
			console.log('THIS IS RESPONSE', response);
		} catch (error) {
			console.error(error);
		}
	};

	// useEffect(() => {
	//     const handleDelete = async () => {
	//         try {
	//             const response = await BeatService.delete(deleteId);
	//             navigate("/profile");
	//             console.log("THIS IS RESPONSE", response);
	//         } catch (error) {
	//             console.error(error);
	//         }
	//     };

	//     if (deleteId !== null) {
	//         handleDelete();
	//     }
	// }, [deleteId, navigate]);

	return (
		<tr
			className="flex cursor-pointer justify-around items-center text-gray-400 transition hover:bg-gray-200 bg-gray-200 bg-opacity-5 hover:bg-opacity-10 rounded-lg my-2 "
			key={id}>
			<td className="flex justify-start items-center">
				<div className="flex p-1">
					{picture ? (
						<img
							src={picture}
							alt={name}
							className="min-w-12 h-12 max-w-12 mr-1 rounded-md duration-300 filter brightness-100 hover:brightness-50"
						/>
					) : (
						<Image
							src={default_picture}
							alt={name}
							className="invert min-w-12 max-w-12 h-12 mr-1 rounded-md duration-300 filter brightness-100 hover:brightness-10"
						/>
					)}
				</div>
				<div className="">
					<a
						onClick={() => {
							dispatch(
								setSong({
									isActive: true,
									currentSong: {
										id: id,
										type: type,
										picture_url: picture,
										author: author,
										name: name,
										album: album,
										date: date,
										src: src,
									},
								})
							);
						}}>
						<p className="text-white font-bold truncate text-lg lg:w-56">
							{name}
						</p>
					</a>
					<Link href={'/'}>
						<a className="text-md font-semibold text-gray-300 hover:text-white hover:cursor-pointer">
							<span>{author}</span>
						</a>
					</Link>
				</div>
			</td>
			<Link href={'/'}>
				<td className="text-sm items-center font-semibold text-center">
					{album}
				</td>
			</Link>
			<td className="text-sm items-center font-semibold text-center">{date}</td>
			<td className="text-sm items-center font-semibold text-center">1:49</td>
			{isAction ? (
				<td className="flex justify-center">
					<div className="p-1">
						<DefaultButton title="Edit" />
					</div>
					<div className="p-1">
						<DefaultButton title="Delete" onClick={() => handleDelete(id)} />
					</div>
				</td>
			) : (
				<></>
			)}
		</tr>
	);
}
